(function () {
  "use strict";

  const data = window.cxWorkbookData;

  const state = {
    chartInstances: []
  };

  const stageOrder = data ? data.pipelineStages.map(stage => stage.name) : [];
  const stageProbabilityMap = data ? Object.fromEntries(data.pipelineStages.map(stage => [stage.name, stage.probability])) : {};

  function byId(id) {
    return document.getElementById(id);
  }

  function formatCurrency(value, precision = 1) {
    if (value >= 1000000) return `${(value / 1000000).toFixed(precision)}M record`;
    return `${Math.round(value / 1000)}k record`;
  }

  function formatProbability(value) {
    return `${Math.round(value * 100)}%`;
  }

  function accountById(id) {
    return data.accounts.find(account => account.id === id);
  }

  function ponderatoFitScore(account) {
    const dimensions = data.scoringMethodology.dimensions;
    const totalWeight = dimensions.reduce((sum, dimension) => sum + dimension.weight, 0);
    const ponderatoTotal = dimensions.reduce((sum, dimension) => {
      return sum + (account.scoreComponents[dimension.key] || 0) * dimension.weight;
    }, 0);
    return ponderatoTotal / totalWeight;
  }

  function dealProbability(deal) {
    return stageProbabilityMap[deal.stage] || 0;
  }

  function ponderatoDealValue(deal) {
    return deal.value * dealProbability(deal);
  }

  function allPipelineValue() {
    return data.pipelineDeals.reduce((sum, deal) => sum + deal.value, 0);
  }

  function allWeightedPipelineValue() {
    return data.pipelineDeals.reduce((sum, deal) => sum + ponderatoDealValue(deal), 0);
  }

  function openDeals() {
    return data.pipelineDeals.filter(deal => !["Action Completed", "Azione Completata", "CX Handoff", "Handoff CX"].includes(deal.stage));
  }

  function average(values) {
    if (!values.length) return 0;
    return values.reduce((sum, value) => sum + value, 0) / values.length;
  }

  function stageAggregates() {
    return stageOrder.map(stage => {
      const deals = data.pipelineDeals.filter(deal => deal.stage === stage);
      const total = deals.reduce((sum, deal) => sum + deal.value, 0);
      const ponderato = deals.reduce((sum, deal) => sum + ponderatoDealValue(deal), 0);
      const avgDays = deals.length ? average(deals.map(deal => deal.daysInStage)) : 0;
      return { stage, deals, total, ponderato, avgDays, probability: stageProbabilityMap[stage] || 0 };
    });
  }

  function setText(id, value) {
    const element = byId(id);
    if (element) element.textContent = value;
  }

  function priorityClass(value) {
    const normalized = String(value || "").toLowerCase();
    if (["high", "alto"].includes(normalized)) return "high";
    if (["medium", "medio"].includes(normalized)) return "medium";
    return "low";
  }

  function setFallbackMetrics() {
    document.querySelectorAll(".kpi-value, .metric-value").forEach(element => {
      if (element.textContent.trim() === "Caricamento...") {
        element.textContent = "Non disponibile";
      }
    });
  }

  function renderKpis() {
    const total = allPipelineValue();
    const ponderato = allWeightedPipelineValue();
    const avgStageAge = average(data.pipelineDeals.map(deal => deal.daysInStage));
    const avgPocReadiness = average(data.pipelineDeals.map(deal => deal.pocReadiness));
    const avgFit = average(data.accounts.map(account => ponderatoFitScore(account)));

    setText("kpi-total-pipeline", formatCurrency(total));
    setText("kpi-weighted-pipeline", formatCurrency(ponderato));
    setText("kpi-accounts", String(data.accounts.length));
    setText("kpi-stage-age", `${avgStageAge.toFixed(1)} giorni`);
    setText("kpi-poc", `${Math.round(avgPocReadiness)}%`);

    setText("dashboard-total-pipeline", formatCurrency(total));
    setText("dashboard-weighted-pipeline", formatCurrency(ponderato));
    setText("dashboard-open-opps", String(openDeals().length));
    setText("dashboard-fit-score", avgFit.toFixed(2));
  }

  function renderInsights() {
    const grid = byId("insights-grid");
    if (!grid) return;

    grid.innerHTML = data.executiveInsights.map((insight, index) => `
      <article class="glass-panel insight-card">
        <div class="eyebrow">Insight ${index + 1}</div>
        <h3>${insight.title}</h3>
        <p><strong>Segnale osservato:</strong> ${insight.signal}</p>
        <p><strong>Rischio operativo:</strong> ${insight.risk}</p>
        <p><strong>Azione raccomandata:</strong> ${insight.action}</p>
        <p><strong>Impatto atteso:</strong> ${insight.impact.replace("Impatto atteso: ", "")}</p>
      </article>
    `).join("");
  }

  function renderReviewPaths() {
    const grid = byId("review-paths-grid");
    if (!grid || !Array.isArray(data.reviewPaths)) return;

    grid.innerHTML = data.reviewPaths.map(path => `
      <article class="glass-panel review-path-card">
        <div class="eyebrow">Percorso di lettura</div>
        <h3>${path.title}</h3>
        <div class="review-path-meta">
          <span class="review-path-label">Ideale per</span>
          <p>${path.bestFor}</p>
        </div>
        <div class="review-path-meta">
          <span class="review-path-label">Cosa guardare</span>
          <p>${path.whatToInspect}</p>
        </div>
        <button class="jump-button review-path-button" type="button" data-nav-target="${path.target}">${path.cta}</button>
      </article>
    `).join("");
  }

  function renderReviewerGuide() {
    const container = byId("reviewer-guide-list");
    if (!container || !Array.isArray(data.reviewerGuide)) return;

    container.innerHTML = data.reviewerGuide.map((item, index) => `
      <article class="checklist-item checked reviewer-guide-item">
        <span class="check-indicator" aria-hidden="true"></span>
        <div class="reviewer-guide-copy">
          <strong>${index + 1}. ${item.title}</strong>
          <p>${item.note}</p>
          <button class="jump-button review-guide-button" type="button" data-nav-target="${item.target}">Apri ${item.title}</button>
        </div>
      </article>
    `).join("");
  }

  function renderStageProbabilities() {
    const container = byId("stage-probability-row");
    if (!container) return;

    container.innerHTML = data.pipelineStages.map(stage => `
      <div class="probability-pill">
        <span>${stage.name}</span>
        <strong>${formatProbability(stage.probability)}</strong>
      </div>
    `).join("");
  }

  function renderKanban() {
    const board = byId("kanban-board");
    if (!board) return;

    board.innerHTML = stageAggregates().map(group => `
      <section class="kanban-column">
        <div class="kanban-header">
          <span>${group.stage}</span>
          <small>${formatProbability(group.probability)}  -  ${formatCurrency(group.ponderato, 2)} ponderato</small>
        </div>
        <div class="kanban-cards">
          ${group.deals.length ? group.deals.map(deal => {
            const account = accountById(deal.accountId);
            return `
              <article class="kanban-card">
                <div class="card-title">${account ? account.company : "Segmento sconosciuto"}</div>
                <div class="card-value">${formatCurrency(deal.value, 2)} <span>${formatCurrency(ponderatoDealValue(deal), 2)} ponderato</span></div>
                <div class="card-meta">
                  <span><i class="fa-regular fa-clock"></i>${deal.daysInStage} giorni</span>
                  <span><i class="fa-solid fa-triangle-exclamation"></i>${deal.risk}</span>
                </div>
                <div class="card-next"><strong>Prossimo step:</strong> ${deal.nextStep}</div>
              </article>
            `;
          }).join("") : `<div class="empty-column">Nessuna analisi simulata</div>`}
        </div>
      </section>
    `).join("");
  }

  function renderExitCriteria() {
    const container = byId("exit-criteria-grid");
    if (!container) return;

    container.innerHTML = data.stageExitCriteria.map(item => `
      <article class="glass-panel criteria-card">
        <h3>${item.transition}</h3>
        <ul>
          ${item.criteria.map(criterion => `<li>${criterion}</li>`).join("")}
        </ul>
      </article>
    `).join("");
  }

  function renderScoring() {
    const formula = byId("scoring-formula");
    const weights = byId("scoring-weights");
    const body = document.querySelector("#scoring-table tbody");
    if (!formula || !weights || !body) return;

    formula.textContent = data.scoringMethodology.formula;

    weights.innerHTML = data.scoringMethodology.dimensions.map(dimension => `
      <article class="weight-card">
        <div class="weight-value">${dimension.weight}%</div>
        <h4>${dimension.label}</h4>
        <p>${dimension.definition}</p>
      </article>
    `).join("");

    const sortedAccounts = [...data.accounts].sort((a, b) => ponderatoFitScore(b) - ponderatoFitScore(a));
    body.innerHTML = sortedAccounts.map(account => {
      const score = ponderatoFitScore(account);
      const components = data.scoringMethodology.dimensions.map(d => account.scoreComponents[d.key]).join(" / ");
      const priority = String(account.regulatorySensitivity || "").toLowerCase();
      const badgeClass = ["high", "alto"].includes(priority) ? "badge-high" : ["medium", "medio"].includes(priority) ? "badge-medium" : "badge-low";

      return `
        <tr>
          <td><strong>${account.company}</strong><br><small>${account.type}</small></td>
          <td>${account.sector}</td>
          <td><span class="badge ${badgeClass}">${account.regulatorySensitivity}</span></td>
          <td>${account.dataComplexityLabel}</td>
          <td><strong>${score.toFixed(2)}</strong></td>
          <td><span class="mono">${components}</span></td>
          <td>${account.useCasePotential}</td>
        </tr>
      `;
    }).join("");
  }

  function renderBriefSimulator() {
    const select = byId("account-select");
    const generateBtn = byId("generate-brief");
    const output = byId("brief-output");
    const promptList = byId("brief-prompt-structure");
    if (!select || !generateBtn || !output || !promptList) return;

    select.innerHTML = `<option value="">Seleziona segmento cliente</option>` + data.accounts
      .map(account => `<option value="${account.id}">${account.company}  -  ${account.sector}</option>`)
      .join("");

    promptList.innerHTML = data.briefPromptStructure.map(item => `<li>${item}</li>`).join("");

    generateBtn.addEventListener("click", () => {
      const selectedId = Number(select.value);
      const account = accountById(selectedId);
      if (!account) {
        output.innerHTML = `<div class="empty-state">Seleziona un segmento cliente per generare l'output strutturato del simulatore.</div>`;
        return;
      }

      const score = ponderatoFitScore(account);
      const sectorDriver = data.sectorBuyingDrivers[account.sector] || "soddisfazione cliente, chiarezza del journey, qualità dati e miglioramento processo misurabile";
      const topRisks = [];
      if (account.scoreComponents.procurementFeasibility <= 2) topRisks.push("percorso d'azione poco chiaro");
      if (account.scoreComponents.stakeholderClarity <= 3) topRisks.push("copertura responsabili incompleta");
      if (account.scoreComponents.deploymentFit >= 4) topRisks.push("revisione reporting e qualità fonte");
      if (!topRisks.length) topRisks.push("chiarezza dello scope prima del pilot d'azione");

      output.innerHTML = `
        <article class="brief-card">
          <div class="brief-header">
            <div>
              <div class="eyebrow">Output strutturato del simulatore</div>
              <h3>${account.company}</h3>
            </div>
            <div class="brief-score">Fit ${score.toFixed(2)}</div>
          </div>

          <section>
            <h4>Contesto del segmento cliente</h4>
            <p>${account.reason}</p>
          </section>

          <section>
            <h4>Driver CX probabili</h4>
            <p>Per ${account.sector}, i driver CX probabili includono ${sectorDriver}. L'analisi dovrebbe collegare il segnale cliente a un miglioramento misurabile del journey e a una gestione responsabile dei dati.</p>
          </section>

          <section>
            <h4>Potenziale caso d'uso analytics</h4>
            <p>${account.useCasePotential}. L'obiettivo dovrebbe essere definito come workflow di reporting assistito, con chiara revisione umana e metrica d'azione misurabile.</p>
          </section>

          <section>
            <h4>Stakeholder da coinvolgere</h4>
            <p>${account.decisionMakers}. Aggiungere Data/IT, Privacy e responsabile business prima di passare dall'analisi a un pilot di azione.</p>
          </section>

          <section>
            <h4>Domande di discovery</h4>
            <ul>
              <li>Quale momento del customer journey creerebbe il miglioramento misurabile più chiaro?</li>
              <li>Quali fonti dati sarebbero necessarie e chi approva l'accesso?</li>
              <li>Quali vincoli di campione, valori mancanti, privacy o aggregazione devono essere soddisfatti?</li>
              <li>Quale stakeholder possiede l'azione e quale metrica dovrebbe cambiare dopo il follow-up?</li>
            </ul>
          </section>

          <section>
            <h4>Rischi di analisi</h4>
            <p>${topRisks.join(", ")}. Questi elementi dovrebbero essere registrati come rischi di reporting prima di assegnare i responsabili delle azioni.</p>
          </section>

          <section>
            <h4>Prossimo step CX raccomandato</h4>
            <p>Procedere solo quando i criteri di uscita dello stage successivo sono soddisfatti: definizione segmento, responsabile, percorso dati, confine di utilizzo dati e metrica di follow-up devono essere espliciti.</p>
          </section>

          <section>
            <h4>Note di handoff insight-azione</h4>
            <p>Documentare segmento, responsabile dati, responsabile azione, metrica target, vincoli di utilizzo dati e prossima data di revisione prima dell'handoff.</p>
          </section>
        </article>
      `;
    });
  }

  function renderPlaybook() {
    const handoff = byId("handoff-checklist");
    const compliance = byId("compliance-checklist");
    if (!handoff || !compliance) return;

    handoff.innerHTML = data.handoffChecklist.map((item, index) => `
      <li class="checklist-item ${index < 3 ? "checked" : ""}">
        <span class="check-indicator"></span>
        <div>
          <strong>${item.title}</strong>
          <p>${item.desc}</p>
        </div>
      </li>
    `).join("");

    compliance.innerHTML = data.complianceChecklist.map(item => `
      <li class="checklist-item">
        <span class="check-indicator muted"></span>
        <div><p>${item}</p></div>
      </li>
    `).join("");
  }

  function renderBottlenecks() {
    const body = document.querySelector("#bottlenecks-table tbody");
    if (!body) return;

    body.innerHTML = data.bottlenecks.map(item => `
      <tr>
        <td><strong>${item.stage}</strong></td>
        <td>${item.signal}</td>
        <td>${item.cause}</td>
        <td>${item.action}</td>
        <td>${item.impact}</td>
      </tr>
    `).join("");
  }

  function renderCaseStudy() {
    const caseStudy = data.caseStudy;
    if (!caseStudy) return;

    setText("case-study-summary", data.project.oneLineSummary);
    setText("case-study-context", caseStudy.context);
    setText("case-study-problem", caseStudy.problem);
    setText("case-study-solution", caseStudy.solution);
    setText("case-study-role", caseStudy.role);
    setText("case-study-value", caseStudy.businessValue);
    setText("case-study-limitations", caseStudy.limitations);
    setText("case-study-next-iteration", caseStudy.nextIteration);

    const outputs = byId("case-study-outputs");
    if (outputs) {
      outputs.innerHTML = caseStudy.outputs.map(item => `
        <article class="glass-panel output-card">
          <p>${item}</p>
        </article>
      `).join("");
    }
  }

  function renderAdoption() {
    const adoption = data.adoptionGovernance;
    if (!adoption) return;

    const stakeholderBody = document.querySelector("#stakeholder-table tbody");
    const rolloutBody = document.querySelector("#rollout-table tbody");
    const deliverablesBody = document.querySelector("#deliverables-table tbody");
    const guardrails = byId("guardrails-list");
    const training = byId("training-list");
    const metrics = byId("adoption-metrics");

    if (stakeholderBody) {
      stakeholderBody.innerHTML = adoption.stakeholderMap.map(item => `
        <tr>
          <td><strong>${item.stakeholder}</strong></td>
          <td>${item.need}</td>
          <td>${item.role}</td>
        </tr>
      `).join("");
    }

    if (rolloutBody) {
      rolloutBody.innerHTML = adoption.rolloutPlan.map(item => `
        <tr>
          <td><strong>${item.phase}</strong></td>
          <td>${item.goal}</td>
          <td>${item.output}</td>
        </tr>
      `).join("");
    }

    if (deliverablesBody) {
      deliverablesBody.innerHTML = adoption.consultingDeliverables.map(item => `
        <tr>
          <td><strong>${item.deliverable}</strong></td>
          <td>${item.purpose}</td>
        </tr>
      `).join("");
    }

    if (guardrails) {
      guardrails.innerHTML = adoption.guardrails.map(item => `
        <li class="checklist-item">
          <span class="reference-kicker">Guardrail</span>
          <p>${item}</p>
        </li>
      `).join("");
    }

    if (training) {
      training.innerHTML = adoption.trainingPlan.map(item => `
        <li class="checklist-item">
          <span class="reference-kicker">Timing: ${item.timing}</span>
          <div>
            <strong>${item.audience}</strong>
            <p>${item.focus}</p>
          </div>
        </li>
      `).join("");
    }

    if (metrics) {
      metrics.innerHTML = adoption.successMetrics.map(item => `
        <article class="glass-panel output-card">
          <p>${item}</p>
        </article>
      `).join("");
    }
  }

  function renderTrainingMaterial() {
    const trainingMaterial = data.trainingMaterial;
    if (!trainingMaterial) return;

    setText("training-material-intro", trainingMaterial.intro);

    const agendaBody = document.querySelector("#training-agenda-table tbody");
    const objectives = byId("learning-objectives-list");
    const slides = byId("slide-outline-grid");

    if (agendaBody) {
      agendaBody.innerHTML = trainingMaterial.workshopAgenda.map(item => `
        <tr>
          <td><strong>${item.slot}</strong></td>
          <td>${item.topic}</td>
          <td>${item.purpose}</td>
        </tr>
      `).join("");
    }

    if (objectives) {
      objectives.innerHTML = trainingMaterial.learningObjectives.map(item => `
        <li class="checklist-item checked">
          <span class="check-indicator"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (slides) {
      slides.innerHTML = trainingMaterial.slideOutline.map(item => `
        <article class="glass-panel output-card">
          <h3>${item.title}</h3>
          <ul class="training-slide-points">
            ${item.points.map(point => `<li>${point}</li>`).join("")}
          </ul>
        </article>
      `).join("");
    }
  }

  function renderProductBrief() {
    const product = data.productBrief;
    if (!product) return;

    setText("product-problem", product.problemStatement);

    const userBody = document.querySelector("#users-table tbody");
    const stories = byId("user-stories");
    const scopeIn = byId("scope-in");
    const scopeOut = byId("scope-out");
    const metrics = byId("product-metrics");
    const backlog = document.querySelector("#backlog-table tbody");
    const decisionLog = document.querySelector("#decision-log-table tbody");

    if (userBody) {
      userBody.innerHTML = product.targetUsers.map(item => `
        <tr>
          <td><strong>${item.user}</strong></td>
          <td>${item.need}</td>
        </tr>
      `).join("");
    }

    if (stories) {
      stories.innerHTML = product.userStories.map(item => `
        <article class="glass-panel story-card">
          <p>${item}</p>
        </article>
      `).join("");
    }

    if (scopeIn) {
      scopeIn.innerHTML = product.mvpScope.inScope.map(item => `
        <li class="checklist-item checked">
          <span class="check-indicator"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (scopeOut) {
      scopeOut.innerHTML = product.mvpScope.outOfScope.map(item => `
        <li class="checklist-item">
          <span class="check-indicator muted"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (metrics) {
      metrics.innerHTML = product.productMetrics.map(item => `
        <li class="checklist-item">
          <span class="check-indicator"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (backlog) {
      backlog.innerHTML = product.backlog.map(item => `
        <tr>
          <td><span class="priority-pill priority-${priorityClass(item.priority)}">${item.priority}</span></td>
          <td><strong>${item.feature}</strong></td>
          <td>${item.reason}</td>
        </tr>
      `).join("");
    }

    if (decisionLog) {
      decisionLog.innerHTML = product.decisionLog.map(item => `
        <tr>
          <td><strong>${item.decision}</strong></td>
          <td>${item.reason}</td>
        </tr>
      `).join("");
    }
  }

  function renderAutomations() {
    const grid = byId("workflow-grid");
    const toolNote = byId("automation-tool-note");
    const automation = data.automationLayer;
    if (!automation || !grid) return;

    grid.innerHTML = automation.workflows.map(flow => `
      <article class="workflow-card">
        <div class="workflow-header">
          <div>
            <h3>${flow.name}</h3>
            ${flow.platform ? `<div class="workflow-platform">${flow.platform}</div>` : ""}
          </div>
          <span class="workflow-trigger">${flow.trigger}</span>
        </div>
        <div class="workflow-section-title">Condizioni</div>
        <ul class="workflow-conditions">
          ${flow.conditions.map(c => `<li>${c}</li>`).join("")}
        </ul>
        <div class="workflow-action">
          <strong>Azione:</strong> ${flow.action} <span style="color:var(--muted)">&middot; ${flow.delay}</span>
        </div>
        <div class="workflow-value"><strong>Valore:</strong> ${flow.value}</div>
      </article>
    `).join("");

    if (toolNote) toolNote.textContent = automation.toolNote;
  }

  function renderResearchNotes() {
    const grid = byId("research-grid");
    const product = data.productBrief;
    if (!grid || !product || !product.researchNotes) return;

    grid.innerHTML = product.researchNotes.map(note => `
      <article class="research-card">
        <div class="research-method">${note.method}</div>
        <h3>Evidenza Chiave</h3>
        <p>${note.finding}</p>
          <div class="research-impact"><strong>Impatto sulla dashboard:</strong> ${note.impact}</div>
      </article>
    `).join("");
  }

  function renderBusinessMetrics() {
    const body = document.querySelector("#business-metrics-table tbody");
    const product = data.productBrief;
    if (!body || !product || !product.businessMetrics) return;

    body.innerHTML = product.businessMetrics.map(item => `
      <tr>
        <td><strong>${item.productMetric}</strong></td>
        <td>${item.businessImpact}</td>
      </tr>
    `).join("");
  }

  function initPdfExport() {
    const btn = byId("export-governance-pdf");
    if (!btn) return;

    btn.addEventListener("click", () => {
      const { jsPDF } = window.jspdf;
      if (!jsPDF) {
        alert("Libreria PDF non caricata. Riprova più tardi.");
        return;
      }

      const doc = new jsPDF({ unit: "pt", format: "a4" });
      const pageWidth = doc.internal.pageSize.getWidth();
      const margin = 40;
      const maxContentY = 720;
      let y = 50;
      const ensurePageSpace = (neededHeight = 0) => {
        if (y + neededHeight > maxContentY) {
          doc.addPage();
          y = 50;
        }
      };

      // Header
      doc.setFillColor(7, 9, 20);
      doc.rect(0, 0, pageWidth, 80, "F");
      doc.setTextColor(42, 211, 167);
      doc.setFontSize(10);
      doc.text("ANALISI CUSTOMER EXPERIENCE", margin, 32);
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(20);
      doc.text("Checklist Qualità Dati Cliente e Privacy", margin, 58);

      y = 100;
      doc.setTextColor(100, 100, 100);
      doc.setFontSize(9);
      doc.text("Ducati CX Analytics Workbook | Caso Studio Portfolio", margin, y);

      y += 22;
      doc.setTextColor(60, 60, 60);
      doc.text("Documento", margin, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Checklist Qualità Dati Cliente e Privacy", margin + 62, y);
      doc.setTextColor(60, 60, 60);
      doc.text("Versione", pageWidth - 185, y);
      doc.setTextColor(30, 30, 30);
      doc.text("v1.0", pageWidth - 135, y);

      y += 16;
      doc.setTextColor(60, 60, 60);
      doc.text("Data", margin, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Aprile 2026", margin + 62, y);
      doc.setTextColor(60, 60, 60);
      doc.text("Responsabile", pageWidth - 185, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Riccardo Capanna", pageWidth - 135, y);

      y += 16;
      doc.setTextColor(60, 60, 60);
      doc.text("Stato", margin, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Bozza / Per revisione", margin + 62, y);

      y += 26;
      doc.setTextColor(30, 30, 30);
      doc.setFontSize(10);
      doc.text("Questo documento sintetizza controlli di qualità dei dati cliente, privacy guardrail, aspettative di revisione umana e confini di rischio operativo per workflow di analisi Customer Experience.", margin, y, { maxWidth: pageWidth - margin * 2 });

      y += 55;
      doc.setFontSize(13);
      doc.setTextColor(7, 9, 20);
      doc.text("Guardrail Qualità Dati Cliente e Privacy", margin, y);
      y += 18;

      const guardrails = data.adoptionGovernance.guardrails;
      doc.setFontSize(10);
      guardrails.forEach((g, i) => {
        doc.setTextColor(42, 211, 167);
        doc.text(`${i + 1}.`, margin, y);
        doc.setTextColor(50, 50, 50);
        doc.text(g, margin + 18, y, { maxWidth: pageWidth - margin * 2 - 18 });
        const lines = doc.splitTextToSize(g, pageWidth - margin * 2 - 18).length;
        y += lines * 14 + 10;
        if (y > maxContentY) {
          doc.addPage();
          y = 50;
        }
      });

      y += 20;
      doc.setFontSize(13);
      doc.setTextColor(7, 9, 20);
      doc.text("Checklist Qualità Dati Cliente e Privacy", margin, y);
      y += 18;

      const checklist = data.complianceChecklist;
      const checklistIndexWidth = doc.getTextWidth(`${checklist.length}.`);
      const checklistTextX = margin + checklistIndexWidth + 12;
      const checklistTextWidth = pageWidth - margin - checklistTextX;
      doc.setFontSize(10);
      checklist.forEach((item, i) => {
        doc.setTextColor(81, 122, 255);
        doc.text(`${i + 1}.`, margin, y);
        doc.setTextColor(50, 50, 50);
        doc.text(item, checklistTextX, y, { maxWidth: checklistTextWidth });
        const checklistLines = doc.splitTextToSize(item, checklistTextWidth).length;
        y += checklistLines * 14 + 10;
        if (y > maxContentY) {
          doc.addPage();
          y = 50;
        }
      });

      const escalationRule = data.complianceEscalationRule;
      const escalationLines = doc.splitTextToSize(escalationRule, pageWidth - margin * 2 - 20);
      ensurePageSpace(escalationLines.length * 12 + 34);
      doc.setFillColor(248, 243, 231);
      doc.roundedRect(margin, y, pageWidth - margin * 2, escalationLines.length * 12 + 22, 8, 8, "F");
      doc.setTextColor(120, 88, 32);
      doc.setFontSize(9);
      doc.text(escalationLines, margin + 10, y + 15);
      y += escalationLines.length * 12 + 34;

      y += 25;
      ensurePageSpace(110);
      doc.setFontSize(13);
      doc.setTextColor(7, 9, 20);
      doc.text("Sintesi Guida al Reporting", margin, y);
      y += 18;

      const training = data.adoptionGovernance.trainingPlan;
      const trainingLabelWidth = 170;
      const trainingGutter = 24;
      const trainingLabelRightX = margin + trainingLabelWidth;
      const trainingFocusX = trainingLabelRightX + trainingGutter;
      const trainingFocusWidth = pageWidth - margin - trainingFocusX;
      doc.setFontSize(10);
      training.forEach(t => {
        ensurePageSpace(48);
        doc.setTextColor(7, 9, 20);
        doc.setFont(undefined, "bold");
        doc.text(t.audience, trainingLabelRightX, y, { align: "right" });
        doc.setFontSize(8);
        doc.setFont(undefined, "normal");
        doc.setTextColor(120, 120, 120);
        doc.text(t.timing, trainingLabelRightX, y + 11, { align: "right" });
        doc.setFontSize(10);
        doc.setFont(undefined, "normal");
        doc.setTextColor(80, 80, 80);
        doc.text(t.focus, trainingFocusX, y, { maxWidth: trainingFocusWidth });
        const lines = doc.splitTextToSize(t.focus, trainingFocusWidth).length;
        y += Math.max(lines * 14, 24) + 10;
        if (y > maxContentY) {
          doc.addPage();
          y = 50;
        }
      });

      // Footer
      const totalPages = doc.internal.getNumberOfPages();
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(`Pagina ${i} di ${totalPages} | Ducati CX Analytics Workbook | Caso Studio`, margin, 810);
        doc.text("Dati simulati | Non è una valutazione legale privacy", pageWidth - margin, 810, { align: "right" });
      }

      doc.save("Checklist_Qualita_Dati_Cliente_Privacy_CX_Analytics.pdf");
    });
  }

  function renderMethodology() {
    const container = byId("methodology-grid");
    if (!container) return;

    container.innerHTML = data.methodologySections.map(section => `
      <article class="glass-panel methodology-card">
        <h3>${section.title}</h3>
        <ul>
          ${section.items.map(item => `<li>${item}</li>`).join("")}
        </ul>
      </article>
    `).join("");
  }

  function chartFallback() {
    document.querySelectorAll(".chart-container").forEach(container => {
      container.innerHTML = `<div class="chart-fallback">I grafici richiedono Chart.js. I valori sottostanti sono comunque mostrati nelle KPI card e nelle tabelle.</div>`;
    });
  }

  function resetCharts() {
    state.chartInstances.forEach(chart => chart.destroy());
    state.chartInstances = [];
  }

  function renderCharts() {
    if (typeof Chart === "undefined") {
      chartFallback();
      return;
    }

    resetCharts();
    Chart.defaults.color = "rgba(180, 189, 208, 0.72)";
    Chart.defaults.font.family = "Inter, Arial, sans-serif";

    const aggregates = stageAggregates();

    state.chartInstances.push(new Chart(byId("pipelineChart"), {
      type: "bar",
      data: {
        labels: aggregates.map(item => item.stage),
        datasets: [
          {
            label: "Volume feedback totale",
            data: aggregates.map(item => Number((item.total / 1000000).toFixed(2))),
            backgroundColor: "rgba(212, 168, 83, 0.55)",
            borderColor: "rgba(212, 168, 83, 1)",
            borderWidth: 1,
            borderRadius: 6
          },
          {
            label: "Volume insight ponderato",
            data: aggregates.map(item => Number((item.ponderato / 1000000).toFixed(2))),
            backgroundColor: "rgba(199, 91, 58, 0.45)",
            borderColor: "rgba(199, 91, 58, 1)",
            borderWidth: 1,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { callback: value => `${value}M unità feedback` } },
          x: { ticks: { maxRotation: 45, minRotation: 0 } }
        },
        plugins: { legend: { labels: { boxWidth: 12 } } }
      }
    }));

    const sectors = data.accounts.reduce((acc, account) => {
      acc[account.sector] = (acc[account.sector] || 0) + 1;
      return acc;
    }, {});

    state.chartInstances.push(new Chart(byId("sectorChart"), {
      type: "doughnut",
      data: {
        labels: Object.keys(sectors),
        datasets: [{
          data: Object.values(sectors),
          backgroundColor: [
            "rgba(212, 168, 83, 0.85)",
            "rgba(199, 91, 58, 0.75)",
            "rgba(180, 140, 80, 0.7)",
            "rgba(160, 100, 60, 0.7)",
            "rgba(120, 80, 50, 0.7)",
            "rgba(100, 120, 160, 0.6)",
            "rgba(180, 189, 208, 0.5)"
          ],
          borderWidth: 0
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: "68%" }
    }));

    state.chartInstances.push(new Chart(byId("daysChart"), {
      type: "line",
      data: {
        labels: aggregates.map(item => item.stage),
        datasets: [{
          label: "Average giorni in current stage",
          data: aggregates.map(item => Number(item.avgDays.toFixed(1))),
          borderColor: "rgba(212, 168, 83, 1)",
          backgroundColor: "rgba(212, 168, 83, 0.12)",
          fill: true,
          tension: 0.35,
          pointRadius: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    }));

    const topAccounts = [...data.accounts]
      .map(account => ({ ...account, score: ponderatoFitScore(account) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 8);

    state.chartInstances.push(new Chart(byId("fitChart"), {
      type: "bar",
      data: {
        labels: topAccounts.map(account => account.company),
        datasets: [{
          label: "Fit score ponderato",
          data: topAccounts.map(account => Number(account.score.toFixed(2))),
          backgroundColor: "rgba(212, 168, 83, 0.5)",
          borderColor: "rgba(212, 168, 83, 1)",
          borderWidth: 1,
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y",
        scales: { x: { beginAtZero: true, max: 5 } }
      }
    }));
  }

  function initNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const jumpButtons = document.querySelectorAll("[data-nav-target]");
    const sections = document.querySelectorAll(".view-section");
    const headerTitle = byId("current-view-title");

    function activateSection(targetId) {
      const targetNav = [...navItems].find(item => item.getAttribute("data-target") === targetId);
      navItems.forEach(nav => nav.classList.toggle("active", nav === targetNav));
      sections.forEach(section => section.classList.toggle("active", section.id === targetId));
      if (headerTitle && targetNav) headerTitle.textContent = targetNav.textContent.trim();
      if (targetId === "commercial-ops") window.requestAnimationFrame(renderCharts);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    navItems.forEach(item => {
      item.addEventListener("click", () => activateSection(item.getAttribute("data-target")));
    });

    jumpButtons.forEach(button => {
      button.addEventListener("click", () => activateSection(button.getAttribute("data-nav-target")));
    });
  }

  function init() {
    if (!data) {
      console.error("cxWorkbookData non è stato caricato. Controlla cx-data.js per errori di sintassi o caricamento.");
      setFallbackMetrics();
      return;
    }

    setText("project-title", data.project.title);
    setText("project-subtitle", data.project.subtitle);
    setText("project-positioning", data.project.positioning);
    setText("hero-review-line", data.project.heroReviewLine);
    setText("project-disclaimer", data.project.disclaimer);
    setText("header-subtitle", data.project.headerSubtitle);
    setText("profile-label", data.project.profileLabel);
    setText("cta-dashboard", data.project.dashboardCta);
    setText("cta-adoption", data.project.adoptionCta);
    setText("cta-product", data.project.productCta);
    setText("scoring-disclaimer", data.project.scoringDisclaimer);
    setText("scoring-scale", data.scoringMethodology.scale);

    renderReviewPaths();
    renderReviewerGuide();
    initNavigation();
    renderKpis();
    renderInsights();
    renderStageProbabilities();
    renderKanban();
    renderExitCriteria();
    renderScoring();
    renderBriefSimulator();
    renderPlaybook();
    renderBottlenecks();
    renderCaseStudy();
    renderAutomations();
    renderAdoption();
    renderTrainingMaterial();
    renderProductBrief();
    renderResearchNotes();
    renderBusinessMetrics();
    initPdfExport();
    renderMethodology();
  }

  document.addEventListener("DOMContentLoaded", () => {
    try {
      init();
    } catch (error) {
      console.error("Inizializzazione workbook non riuscita.", error);
      setFallbackMetrics();
      chartFallback();
    }
  });
})();

