import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

const dataSource = fs.readFileSync(path.join(rootDir, "cx-data.js"), "utf8");
const html = fs.readFileSync(path.join(rootDir, "index.html"), "utf8");
const appSource = fs.readFileSync(path.join(rootDir, "cx-workbook.js"), "utf8");

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(dataSource, sandbox, { filename: "cx-data.js" });

const data = sandbox.window.cxWorkbookData;
const errors = [];

function assert(condition, message) {
  if (!condition) errors.push(message);
}

function nonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function assertNonEmptyString(value, message) {
  assert(nonEmptyString(value), message);
}

function assertNonEmptyArray(value, message) {
  assert(Array.isArray(value) && value.length > 0, message);
}

function collectAttributeValues(source, attribute) {
  return [...source.matchAll(new RegExp(`${attribute}="([^"]+)"`, "g"))].map(match => match[1]);
}

assert(data && typeof data === "object", "cxWorkbookData was not loaded from cx-data.js");

if (data) {
  const dimensions = data.scoringMethodology?.dimensions ?? [];
  const accounts = data.accounts ?? [];
  const deals = data.pipelineDeals ?? [];
  const stages = data.pipelineStages ?? [];
  const stageExitCriteria = data.stageExitCriteria ?? [];
  const demoScenarios = data.demoScenarios ?? [];
  const sectionIds = new Set(collectAttributeValues(html, "id"));
  const navTargets = new Set([
    ...collectAttributeValues(html, "data-target"),
    ...collectAttributeValues(html, "data-nav-target")
  ]);

  const dimensionKeys = new Set(dimensions.map(dimension => dimension.key));
  const accountIds = new Set(accounts.map(account => account.id));
  const stageNames = new Set(stages.map(stage => stage.name));
  const stageProbability = new Map(stages.map(stage => [stage.name, stage.probability]));

  assertNonEmptyArray(data.reviewPaths, "reviewPaths must not be empty");
  assertNonEmptyArray(data.reviewerGuide, "reviewerGuide must not be empty");
  assertNonEmptyArray(data.methodologySections, "methodologySections must not be empty");
  assertNonEmptyArray(data.complianceChecklist, "complianceChecklist must not be empty");
  assertNonEmptyArray(data.adoptionGovernance?.guardrails, "adoption guardrails must not be empty");
  assertNonEmptyArray(demoScenarios, "demoScenarios must not be empty");

  assert(
    dimensions.reduce((sum, dimension) => sum + (dimension.weight || 0), 0) === 100,
    "scoring weights must sum to 100%"
  );

  assert(new Set(accounts.map(account => account.id)).size === accounts.length, "account IDs must be unique");
  assert(new Set(deals.map(deal => deal.id)).size === deals.length, "deal IDs must be unique");
  assert(new Set(stages.map(stage => stage.name)).size === stages.length, "pipeline stage names must be unique");

  navTargets.forEach(target => {
    assert(sectionIds.has(target), `navigation target "${target}" does not match any section id`);
  });

  ["demo-lab", "cx-demo-segments", "cx-demo-timeline", "cx-demo-prev", "cx-demo-next"].forEach(id => {
    assert(sectionIds.has(id), `required demo element id "${id}" is missing from index.html`);
  });

  assert(appSource.includes("function renderCxDemo"), "cx-workbook.js must define renderCxDemo");
  assert(appSource.includes("renderCxDemo();"), "cx-workbook.js must call renderCxDemo during init");

  stages.forEach(stage => {
    assertNonEmptyString(stage.name, "each pipeline stage must have a name");
    assert(typeof stage.probability === "number" && stage.probability >= 0 && stage.probability <= 1, `stage "${stage.name}" must have a probability between 0 and 1`);
  });

  accounts.forEach(account => {
    assertNonEmptyString(account.company, `account ${account.id} must have a company`);
    assert(account.scoreComponents && typeof account.scoreComponents === "object", `account ${account.id} must have scoreComponents`);
    for (const key of dimensionKeys) {
      const value = account.scoreComponents?.[key];
      assert(typeof value === "number" && value >= 1 && value <= 5, `account ${account.id} is missing a valid score for "${key}"`);
    }
  });

  deals.forEach(deal => {
    assert(accountIds.has(deal.accountId), `deal ${deal.id} references missing account ${deal.accountId}`);
    assert(stageNames.has(deal.stage), `deal ${deal.id} uses unknown stage "${deal.stage}"`);
    assert(typeof deal.value === "number" && deal.value > 0, `deal ${deal.id} must have a positive value`);
    assert(typeof deal.pocReadiness === "number" && deal.pocReadiness >= 0 && deal.pocReadiness <= 100, `deal ${deal.id} must have pocReadiness between 0 and 100`);
    assertNonEmptyString(deal.risk, `deal ${deal.id} must have a risk label`);
    assertNonEmptyString(deal.nextStep, `deal ${deal.id} must have a nextStep`);
  });

  stageExitCriteria.forEach(item => {
    assertNonEmptyString(item.transition, "each stage exit criterion must declare a transition");
    assertNonEmptyArray(item.criteria, `transition "${item.transition}" must include criteria`);

    const normalized = item.transition.replace(/â†’/g, "->").replace(/→/g, "->");
    const [fromStage, toStage] = normalized.split("->").map(part => part?.trim());

    assert(stageNames.has(fromStage), `transition "${item.transition}" references unknown start stage "${fromStage}"`);
    assert(stageNames.has(toStage), `transition "${item.transition}" references unknown end stage "${toStage}"`);
  });

  [...data.reviewPaths, ...data.reviewerGuide].forEach(item => {
    assertNonEmptyString(item.title, "each reviewer route must have a title");
    assert(sectionIds.has(item.target), `review route "${item.title}" targets missing section "${item.target}"`);
  });

  demoScenarios.forEach(scenario => {
    assert(accountIds.has(scenario.accountId), `demo scenario "${scenario.label}" references missing account ${scenario.accountId}`);
    assertNonEmptyString(scenario.label, "each demo scenario must have a label");
    assertNonEmptyString(scenario.owner, `demo scenario "${scenario.label}" must have an owner`);
    assertNonEmptyString(scenario.metric, `demo scenario "${scenario.label}" must have a metric`);
    assertNonEmptyString(scenario.persona, `demo scenario "${scenario.label}" must have a persona`);
    assert(Array.isArray(scenario.steps) && scenario.steps.length >= 3, `demo scenario "${scenario.label}" must have at least 3 steps`);
    scenario.steps.forEach(step => {
      ["title", "stage", "signal", "evidence", "decision", "output"].forEach(key => {
        assertNonEmptyString(step[key], `demo scenario "${scenario.label}" has a step missing "${key}"`);
      });
    });
  });

  const totalVolume = deals.reduce((sum, deal) => sum + deal.value, 0);
  const weightedVolume = deals.reduce((sum, deal) => sum + deal.value * (stageProbability.get(deal.stage) || 0), 0);

  assert(totalVolume > 0, "total feedback volume must be positive");
  assert(weightedVolume > 0, "weighted insight volume must be positive");
  assert(weightedVolume <= totalVolume, "weighted insight volume cannot exceed total feedback volume");

  if (!errors.length) {
console.log(`Industrial CX validation passed: ${accounts.length} segments, ${deals.length} records, ${demoScenarios.length} demo scenarios.`);
    console.log(`Computed volumes: total=${Math.round(totalVolume)} weighted=${Math.round(weightedVolume)}.`);
  }
}

if (errors.length) {
  console.error("Industrial CX validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}
