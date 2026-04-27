(function () {
  "use strict";

  const d = window.cockpitData;
  if (!d) return;

  d.project = {
    title: "Cockpit di analisi dati per Customer Experience",
    subtitle: "Caso studio interattivo statico che mostra come un team Customer Experience potrebbe organizzare reporting di soddisfazione, segmentazione clienti, diagnostica del journey e azioni di miglioramento cross-funzionali.",
    disclaimer: `Questo è un caso studio portfolio indipendente basato su dati Customer Experience simulati.
Non è collegato a sistemi Ducati, non usa dati cliente riservati ed è pensato solo per dimostrare ragionamento analitico, logica dashboard e gestione responsabile dei dati.`,
    positioning: `Ho adattato il cockpit originale in una versione di analisi Customer Experience allineata a un tirocinio Data Analyst.
Il focus è su raccolta e organizzazione dei dati, costruzione di viste di reporting, segmentazione clienti, identificazione dei trend e traduzione degli insight in azioni di miglioramento chiare per i team business.`,
    oneLineSummary: "Caso studio interattivo che mostra come un team Customer Experience potrebbe trasformare comportamento cliente, segnali di soddisfazione e feedback sul journey in dashboard, segmenti, trend e raccomandazioni pronte per l'azione.",
    headerSubtitle: "Analisi Customer Experience · Segmentazione · Reporting",
    profileLabel: "Caso studio per Data Analyst Customer Experience",
    heroReviewLine: "Progettato per essere letto da quattro angoli: reporting di soddisfazione cliente, segmentazione, diagnostica del journey e azioni di miglioramento cross-funzionali.",
    cockpitCta: "Rivedi il livello CX Analytics",
    adoptionCta: "Rivedi il livello insight-azione",
    productCta: "Rivedi il brief dashboard MVP",
    caseStudyCta: "Leggi la sintesi del caso studio",
    scoringDisclaimer: `Punteggi ed esempi di segmento sono illustrativi.
Usano assunzioni simulate di Customer Experience e non rappresentano dati Ducati, valutazioni reali dei clienti o informazioni aziendali riservate.`
  };

  d.caseStudy = {
    context: "Un brand premium automotive o motociclistico ha bisogno di modalità strutturate per comprendere soddisfazione cliente, esperienza service, comportamento digitale, follow-up dealer e segnali del journey dei proprietari su più touchpoint.",
    problem: "I dati cliente possono essere frammentati tra survey, note CRM, interazioni dealer, form digitali, record service e feedback di campagna. Senza un workflow di reporting ripetibile, i team possono perdere pain point ricorrenti o faticare a comunicare chiaramente i risultati.",
    solution: "Ho progettato un cockpit simulato di analisi Customer Experience che combina data intake, scoring dei segmenti, tracking degli stage del journey, diagnosi dei trend, dashboard reporting, guardrail privacy-aware e logica di handoff verso azione.",
    role: `Ho definito framing analitico, dimensioni di scoring, struttura del workflow, narrativa dashboard e documentazione per valutatori.
La logica dati, il framing CX, la struttura del progetto e l'adattamento del caso d'uso sono stati definiti in modo indipendente.`,
    businessValue: "Il caso studio mostra come un team CX potrebbe standardizzare la revisione della soddisfazione cliente, prioritizzare segmenti ad alto impatto, rilevare frizioni nel journey, comunicare insight in modo chiaro e coordinare azioni di miglioramento con stakeholder CRM, rete dealer, service, marketing e product.",
    limitations: "Il progetto usa dati simulati, non ha integrazione CRM live ed è pensato come prototipo portfolio, non come sistema analytics di produzione.",
    nextIteration: "In un contesto operativo reale, la prossima iterazione aggiungerebbe integrazione CRM o survey, reporting in stile Power BI, viste per ruolo, refresh automatici, controlli di qualità dati, controlli privacy cliente e misurazione del feedback loop dopo le azioni.",
    outputs: [
      "Scoring dei segmenti cliente e prioritizzazione data-driven.",
      "Analisi degli stage del journey con volume insight totale vs ponderato.",
      "Diagnosi di trend e colli di bottiglia collegata ad azioni concrete di Customer Experience.",
      "Workflow di handoff CX-business per team service, dealer, CRM e product.",
      "Tracker insight-azione con privacy guardrail, note di guida al reporting e KPI di follow-up.",
      "Brief dashboard MVP con utenti, perimetro MVP, metriche, backlog e note di validazione.",
      "Metodologia trasparente che separa dati cliente simulati e assunzioni portfolio."
    ]
  };

  d.reviewPaths = [
    {
      title: "Analisi soddisfazione cliente",
      bestFor: "Valutatori Customer Experience, CRM e Data Analyst che cercano evidenze di reporting, dashboard e comunicazione degli insight.",
      whatToInspect: "Scoring segmenti, volume insight ponderato, driver di soddisfazione, segnali di trend e confini metodologici.",
      target: "commercial-ops",
      cta: "Rivedi il livello CX Analytics"
    },
    {
      title: "Segmentazione e Profilazione",
      bestFor: "Team che valutano se i gruppi cliente possono essere organizzati in priorità d'azione significative.",
      whatToInspect: "Segmenti cliente, componenti di score, categorie journey, volume feedback e logica di next action.",
      target: "commercial-ops",
      cta: "Rivedi lo scoring segmenti"
    },
    {
      title: "Flusso di miglioramento journey",
      bestFor: "Team business, service, rete dealer e product che valutano ragionamento di miglioramento processo.",
      whatToInspect: "Stage del journey, colli di bottiglia, action pilot, checklist di handoff, automazioni e documentazione operativa.",
      target: "commercial-ops",
      cta: "Rivedi il livello flusso"
    },
    {
      title: "Vista dashboard MVP",
      bestFor: "Team che valutano dashboard design, scope MVP, bisogni utenti e adozione misurabile del reporting.",
      whatToInspect: "Framing del problema, utenti, scope MVP, metriche dashboard, backlog e note di validazione.",
      target: "product",
      cta: "Rivedi il brief dashboard MVP"
    }
  ];

  d.reviewerGuide = [
    {
      title: "Sintesi del Caso Studio",
      note: "Parti da qui per una sintesi di due minuti su contesto, problema, soluzione, output e limiti per un ruolo CX analytics.",
      target: "case-study"
    },
    {
      title: "Scoring dei Segmenti Cliente",
      note: "Rivedi il modello di scoring ponderato, priorità dei segmenti, assunzioni di qualità dati e logica di actionability.",
      target: "commercial-ops"
    },
    {
      title: "Diagnostica Journey",
      note: "Analizza stage del workflow, segnali di bottleneck, bisogni di handoff service/dealer e azioni raccomandate.",
      target: "commercial-ops"
    },
    {
      title: "Tracker insight-azione",
      note: "Rivedi mappatura stakeholder, privacy guardrail, fasi di rollout, focus reporting e KPI di follow-up.",
      target: "adoption"
    },
    {
      title: "Simulatore brief insight",
      note: "Vedi come un brief strutturato può trasformare input dati approvati in una sintesi insight cliente revisionata da una persona.",
      target: "commercial-ops"
    },
    {
      title: "Guida al Reporting",
      note: "Apri agenda esempio, obiettivi di apprendimento e outline slide per una sessione di enablement CX analytics.",
      target: "training-material"
    },
    {
      title: "Metodologia",
      note: "Controlla i confini dei dati simulati e le dichiarazioni non-production prima di valutare la dashboard come evidenza.",
      target: "methodology"
    }
  ];

  d.adoptionGovernance = {
    stakeholderMap: [
      {
        stakeholder: "Team Customer Experience",
        need: "Viste affidabili sulla soddisfazione, priorità segmenti chiare e visibilità dei trend ricorrenti.",
        role: "Responsabile degli insight"
      },
      {
        stakeholder: "CRM / Marketing",
        need: "Profili cliente segmentati, feedback di campagna e logica di follow-up.",
        role: "Partner di attivazione"
      },
      {
        stakeholder: "Rete dealer / Retail operations",
        need: "Feedback azionabili su follow-up, consegna, test ride e esperienza service.",
        role: "Responsabile processo frontline"
      },
      {
        stakeholder: "Service / After-sales",
        need: "Segnali su frizioni di appuntamento, problemi garanzia e soddisfazione post-service.",
        role: "Responsabile del miglioramento"
      },
      {
        stakeholder: "Team Product / Digital",
        need: "Pain point cliente ricorrenti legati ad app, configuratore, connected services o feedback prodotto.",
        role: "Partner di miglioramento experience"
      },
      {
        stakeholder: "Data / IT / Privacy",
        need: "Qualità dati, chiarezza fonti, controlli accesso e gestione responsabile delle informazioni cliente.",
        role: "Enabler qualità dati e privacy"
      }
    ],
    rolloutPlan: [
      {
        phase: "Discovery",
        goal: "Comprendere i dati disponibili da survey, CRM, service, dealer e touchpoint digitali.",
        output: "Mappa fonti dati, note stakeholder, use case prioritari e stage del customer journey."
      },
      {
        phase: "Prototipo",
        goal: "Testare una vista reporting simulata con un piccolo gruppo di stakeholder CX, CRM e service.",
        output: "Feedback, metriche mancanti, note di qualità dati e backlog di refinement."
      },
      {
        phase: "Routine di Reporting",
        goal: "Definire una cadenza ripetibile per revisione dashboard, note insight e tracking azioni.",
        output: "Template di revisione settimanale o mensile e lista responsabili."
      },
      {
        phase: "Revisione privacy",
        goal: "Validare confini dei dati cliente, regole di aggregazione e responsabilità di accesso.",
        output: "Checklist uso dati e logica di escalation."
      },
      {
        phase: "Action Loop",
        goal: "Tradurre insight in pilot di miglioramento e misurare se il segnale cliente cambia.",
        output: "Tracker azioni, vista KPI post-azione e lezioni apprese."
      }
    ],
    guardrails: [
      "Lo scoring dei segmenti deve supportare la prioritizzazione, non sostituire il giudizio umano su clienti o dealer.",
      "I dati personali dei clienti devono essere minimizzati, aggregati dove possibile e gestiti solo tramite sistemi approvati.",
      "I risultati dashboard devono essere controllati per campione, valori mancanti e bias survey prima di essere condivisi come evidenze.",
      "Le bozze di sintesi insight cliente devono essere etichettate chiaramente come materiale di supporto e revisionate da un responsabile umano.",
      "Il feedback cliente deve essere usato per migliorare processi, non per formulare assunzioni individuali non supportate.",
      "La qualità dei dati CRM, survey e dealer deve essere controllata prima di confrontare segmenti o stage del journey.",
      "Usi poco chiari di dati personali devono essere escalati a Privacy, Legal o Data/IT prima di ogni pilot."
    ],
    trainingPlan: [
      {
        audience: "Team Customer Experience",
        timing: "Prototipo onboarding + monthly refresh",
        focus: "Come interpretare score dei segmenti, segnali di trend, limiti di confidenza e azioni raccomandate."
      },
      {
        audience: "CRM / Marketing",
        timing: "Prima della pianificazione campagne o follow-up",
        focus: "Come segmenti e driver di soddisfazione possono informare messaging, timing e logica di follow-up."
      },
      {
        audience: "Stakeholder Service / Dealer",
        timing: "Workshop pre-azione",
        focus: "Come leggere i bottleneck del journey e tradurli in cambiamenti pratici di processo."
      },
      {
        audience: "Data / IT / Privacy",
        timing: "Prima di passare dal prototipo ai dati reali",
        focus: "Come applicare sistemi fonte, controlli accesso, aggregazione e controlli di uso responsabile dei dati."
      }
    ],
    successMetrics: [
      "Utenti attivi settimanali o mensili che rivedono il cockpit CX.",
      "Percentuale di segmenti rivisti con note esplicite su fonte dati e campione.",
      "Riduzione dei pain point ricorrenti non risolti negli stage prioritari del journey.",
      "Tempo di preparazione dashboard per reporting CX.",
      "Tasso di completamento handoff insight-azione.",
      "Numero di azioni di miglioramento con responsabile nominato e metrica di follow-up.",
      "Soddisfazione stakeholder sulla chiarezza del reporting.",
      "Percentuale di bozze di insight summary riviste da una persona prima dell'uso."
    ],
    consultingDeliverables: [
      {
        deliverable: "Mappa dati customer journey",
        purpose: "Comprendere dove segnali survey, CRM, dealer, service e digital entrano nel workflow."
      },
      {
        deliverable: "Modello di prioritizzazione segmenti",
        purpose: "Ordinare gruppi cliente per impatto sulla soddisfazione, confidenza dati e actionability."
      },
      {
        deliverable: "Checklist Qualità Dati Cliente e Privacy",
        purpose: "Definire guardrail di aggregazione, privacy, revisione umana ed escalation."
      },
      {
        deliverable: "Guida al reporting",
        purpose: "Supportare una revisione dashboard coerente da parte di stakeholder CX, CRM, service e dealer."
      },
      {
        deliverable: "Guida al reporting",
        purpose: "Mostrare come agenda workshop e storyline slide supporterebbero un uso coerente del workflow di reporting."
      },
      {
        deliverable: "Tracker KPI azioni",
        purpose: "Misurare se gli insight diventano cambiamenti di processo e se i segnali cliente migliorano."
      }
    ]
  };

  d.trainingMaterial = {
    intro: "Questa guida al reporting mostra il tipo di artefatto per analyst che preparerei prima di un pilot di reporting CX analytics: agenda, obiettivi di apprendimento e semplice storyline slide focalizzata su dati cliente, interpretazione e follow-up delle azioni.",
    workshopAgenda: [
      {
        slot: "0-10 min",
        topic: "Perche questo workflow di reporting conta",
        purpose: "Allinearsi su soddisfazione cliente, frizioni del journey e cosa il team vuole migliorare."
      },
      {
        slot: "10-20 min",
        topic: "Walkthrough delle fonti dati",
        purpose: "Rivedere segnali survey, CRM, service, dealer e digitali più i limiti noti di qualità dati."
      },
      {
        slot: "20-35 min",
        topic: "Interpretazione segmenti e trend",
        purpose: "Spiegare dimensioni di scoring, flag di trend, limiti di confidenza e come evitare over-reading dei dati."
      },
      {
        slot: "35-50 min",
        topic: "Revisione insight-azione",
        purpose: "Rivedere un brief segmento simulato e decidere quale team deve possedere la prossima azione."
      },
      {
        slot: "50-60 min",
        topic: "Cadenza e follow-up",
        purpose: "Confermare responsabile del reporting, campi tracker azioni, cadenza di revisione e prossimi controlli qualità dati."
      }
    ],
    learningObjectives: [
      "Spiegare il workflow target del customer journey e dove l analytics supporta le decisioni.",
      "Riconoscere limiti di qualità dati come campione, valori mancanti, bias e fonti frammentate.",
      "Usare il simulatore di brief insight come materiale di supporto strutturato, non come conclusione automatica.",
      "Identificare condizioni minime di dati, responsabile e metrica di successo prima che un pilot di miglioramento proceda.",
      "Uscire dalla sessione con azioni di follow-up, responsabile e metriche di adozione chiare."
    ],
    slideOutline: [
      {
        title: "Slide 1 - Contesto customer journey",
        points: [
          "Quali momenti cliente sono monitorati",
          "Dove emerge frizione oggi",
          "Come appare il successo in termini cliente e operativi"
        ]
      },
      {
        title: "Slide 2 - Fonti dati e limiti qualità",
        points: [
          "Quali input sono approvati",
          "Quali dati sono mancanti o incoerenti",
          "Come sono documentati campione e bias"
        ]
      },
      {
        title: "Slide 3 - Scoring segmenti e logica trend",
        points: [
          "Quali dimensioni guidano la prioritizzazione",
          "Come sono interpretati gli score",
          "Quali segnali richiedono validazione umana"
        ]
      },
      {
        title: "Slide 4 - Da insight ad azione",
        points: [
          "Come scrivere una evidenza pronta per l'azione",
          "Chi possiede il follow-up",
          "Quale metrica dovrebbe cambiare dopo l'azione"
        ]
      },
      {
        title: "Slide 5 - Cadenza reporting e prossimi step",
        points: [
          "Azioni immediate dopo il workshop",
          "Chi possiede refresh dashboard e note",
          "Quali KPI di adozione saranno monitorati per primi"
        ]
      }
    ]
  };

  d.automationLayer = {
    title: "Flussi di follow-up Customer Experience",
    subtitle: "Come i segnali cliente potrebbero attivare follow-up, assegnazione dei responsabili e routine di reporting.",
    description: "Questa sezione mostra come i segnali operativi del cockpit potrebbero collegarsi a strumenti no-code o low-code per ridurre follow-up manuale e rendere più coerente il tracking insight-azione.",
    workflows: [
      {
        platform: "Power Automate / Zapier",
        name: "Alert Segmento a Bassa Soddisfazione",
        trigger: "Un segmento prioritario scende sotto la soglia di soddisfazione",
        conditions: ["Score ponderato >= 4.0", "Trend soddisfazione negativo", "Campione sopra soglia minima"],
        action: "Notificare il responsabile CX e creare un item tracker azioni con segmento, driver e data target di follow-up",
        delay: "Stesso giorno",
        value: "Trasforma pain point cliente ricorrenti in azioni di revisione assegnate invece che osservazioni passive in dashboard."
      },
      {
        platform: "n8n / Make",
        name: "Digest Follow-up Dealer",
        trigger: "Ciclo di revisione settimanale",
        conditions: ["Esiste feedback legato al dealer", "Action item aperti > 0", "Responsabile assegnato"],
        action: "Inviare un digest a dealer operations con segnali principali, stage del journey coinvolti e azioni non risolte",
        delay: "Settimanale",
        value: "Migliora la visibilità tra CX centrale e team retail frontline."
      },
      {
        platform: "Power Automate",
        name: "Revisione privacy Check",
        trigger: "Viene proposta una nuova fonte dati cliente",
        conditions: ["Dati personali coinvolti", "Metodo di aggregazione poco chiaro", "Responsabile dell'accesso non nominato"],
        action: "Instradare una checklist a Data/IT/Privacy prima che la fonte sia usata nel reporting",
        delay: "Prima dell uso nel pilot",
        value: "Mantiene esplicita la gestione dei dati cliente prima che il workflow superi il prototipo."
      },
      {
        platform: "n8n / Zapier",
        name: "Reminder Action Pilot",
        trigger: "Viene creata un azione di miglioramento",
        conditions: ["Scadenza in avvicinamento", "Metrica di follow-up mancante o non aggiornata"],
        action: "Ricordare al responsabile azione di aggiornare stato, metrica e note di evidenza",
        delay: "48h prima della scadenza",
        value: "Chiude il ciclo tra generazione insight e miglioramento processo misurabile."
      },
      {
        platform: "Copilot Studio",
        name: "Assistente FAQ Post-Workshop",
        trigger: "Uno stakeholder chiede come leggere un segnale dashboard",
        conditions: ["Guida di reporting approvata disponibile", "Percorso di escalation al responsabile CX definito"],
        action: "Rispondere a domande interpretative ricorrenti ed escalare questioni ambigue su dati o privacy a un responsabile umano",
        delay: "Su richiesta",
        value: "Supporta l adozione mantenendo interpretazione e decisioni di uso dati revisionate da una persona."
      }
    ],
    toolNote: "Questi workflow sono progettati per strumenti no-code o low-code come Power Automate, n8n, Make, Zapier e Copilot Studio. Richiedono fonti dati approvate, responsabili chiari e controlli privacy prima di usare dati cliente reali."
  };

  d.productBrief = {
    problemStatement: "I team Customer Experience hanno bisogno di un modo strutturato per combinare survey, CRM, dealer, service e segnali digitali in dashboard chiare, segmenti cliente, spiegazioni dei trend e tracciamento azioni.",
    targetUsers: [
      {
        user: "Analyst Customer Experience",
        need: "Organizzare segnali cliente frammentati in report ricorrenti e evidenze pronte per l'azione."
      },
      {
        user: "CX manager",
        need: "Identificare segmenti cliente prioritari, pain point ricorrenti e responsabili delle azioni di miglioramento."
      },
      {
        user: "Stakeholder CRM / Marketing",
        need: "Capire quali profili cliente o momenti del journey dovrebbero influenzare la strategia di follow-up."
      },
      {
        user: "Service / Dealer operations",
        need: "Ricevere segnali di feedback chiari e specifici traducibili in cambiamenti di processo."
      },
      {
        user: "Valutatore Data / Privacy",
        need: "Vedere assunzioni sulle fonti, logica di aggregazione e confini di uso responsabile dei dati."
      }
    ],
    userStories: [
      "Come CX analyst, voglio identificare driver di soddisfazione ricorrenti per segmento, così posso preparare note di reporting più chiare.",
      "Come CX manager, voglio vedere quali gruppi cliente richiedono attenzione, così posso prioritizzare azioni di miglioramento.",
      "Come stakeholder CRM, voglio insight a livello segmento, così le campagne di follow-up sono più coerenti con il contesto cliente.",
      "Come stakeholder service o dealer, voglio segnali specifici del journey, così i team operativi possono agire sui giusti punti di frizione.",
      "Come valutatore data o privacy, voglio guardrail chiari, così le informazioni cliente sono gestite responsabilmente."
    ],
    mvpScope: {
      inScope: [
        "Dati simulati dei segmenti cliente e modello di scoring.",
        "Overview degli stage del journey e volume insight ponderato.",
        "Diagnosi trend e checklist di handoff azione.",
        "Simulatore di brief insight cliente.",
        "Checklist uso dati privacy-aware.",
        "Prototipo frontend statico per revisione portfolio."
      ],
      outOfScope: [
        "Integrazione live con sistemi Ducati, CRM, dealer o survey.",
        "Profilazione individuale dei clienti o decisioni cliente automatizzate.",
        "Autenticazione, controlli accesso o pipeline dati di produzione.",
        "Deploy Power BI reale.",
        "Valutazione legale privacy."
      ]
    },
    productMetrics: [
      "Completamento della cadenza di revisione dashboard.",
      "Utilizzo settimanale per ruolo.",
      "Percentuale di segmenti con note su fonte dati e campione.",
      "Tasso di completamento handoff insight-azione.",
      "Tempo da rilevazione trend ad assegnazione del responsabile.",
      "Numero di azioni con misurazione post-azione.",
      "Soddisfazione stakeholder sulla chiarezza del report."
    ],
    backlog: [
      {
        priority: "Alto",
        feature: "Export report in stile Power BI",
        reason: "Allinea il prototipo ai workflow di reporting comuni nei ruoli Data Analyst."
      },
      {
        priority: "Alto",
        feature: "Pannello qualità dati",
        reason: "Mostra valori mancanti, campione, freschezza fonte e note di confidenza prima di trarre conclusioni."
      },
      {
        priority: "Medio",
        feature: "Drill-down segmento",
        reason: "Permette ai valutatori di analizzare come soddisfazione, comportamento e stage del journey differiscono tra gruppi cliente."
      },
      {
        priority: "Medio",
        feature: "Storico tracker azioni",
        reason: "Collega generazione insight, miglioramento processo e misurazione follow-up."
      },
      {
        priority: "Basso",
        feature: "Mock integration CRM o survey",
        reason: "Renderebbe il flusso dati più realistico senza richiedere dati riservati."
      }
    ],
    researchNotes: [
      {
        method: "Mappatura Requisiti Annuncio",
        evidenza: "Il tirocinio target richiede raccolta, organizzazione, analisi, reporting, segmentazione clienti e comunicazione chiara.",
        impact: "Ha portato a una versione CX analytics focalizzata su dashboarding, prioritizzazione segmenti, diagnosi trend e handoff azioni."
      },
      {
        method: "Framing Customer Journey",
        evidenza: "Una brand experience premium dipende da più touchpoint: discovery, acquisto, consegna, service, supporto digitale e loyalty.",
        impact: "Ha portato a una logica per stage del journey e categorie di segmenti cliente, non a una pipeline solo sales."
      },
      {
        method: "Revisione uso responsabile dei dati",
        evidenza: "La customer analytics deve gestire con attenzione privacy, aggregazione, campione e limiti interpretativi.",
        impact: "Ha portato a guardrail espliciti, controlli uso dati e note metodologiche sui dati simulati."
      }
    ],
    businessMetrics: [
      { productMetric: "Tempo preparazione dashboard", businessImpact: "Reporting CX ricorrente più rapido" },
      { productMetric: "Completamento handoff insight-azione", businessImpact: "Responsabilità più coerente delle azioni di miglioramento" },
      { productMetric: "Rilevazione trend segmento", businessImpact: "Identificazione anticipata di frizioni ricorrenti nel journey" },
      { productMetric: "Misurazione post-azione", businessImpact: "Collegamento più chiaro tra analytics e miglioramento customer experience" }
    ],
    decisionLog: [
      {
        decision: "Mantenere dati simulati",
        reason: "Il progetto deve dimostrare analisi e comunicazione senza usare informazioni cliente riservate."
      },
      {
        decision: "Usare segmenti cliente invece di clienti individuali",
        reason: "L'analisi a livello segmento è più adatta a un portfolio e supporta un framing attento alla privacy."
      },
      {
        decision: "Mantenere l architettura statica originale",
        reason: "L'obiettivo è dimostrare ragionamento analitico e struttura dashboard, non costruire un backend sovradimensionato."
      },
      {
        decision: "Prioritizzare Power BI e miglioramenti qualità dati nel backlog",
        reason: "Queste aggiunte renderebbero il prototipo ancora più vicino a un tirocinio Data Analyst Customer Experience."
      }
    ]
  };

  d.scoringMethodology = {
    formula: "CX Fit Score = Impatto soddisfazione x 30% + Priorità cliente x 20% + Complessità dati x 15% + Chiarezza responsabile x 15% + Fit reporting x 10% + Actionability x 10%",
    scale: `Ogni variabile è valutata da 1 a 5.
Il punteggio finale è una media ponderata sulla stessa scala 1-5.`,
    dimensions: [
      {
        key: "useCaseValue",
        label: "Impatto Soddisfazione",
        weight: 30,
        definition: "1 = segnale CX debole o poco chiaro. 5 = segmento o issue di journey chiara, ad alto impatto e con valore cliente misurabile."
      },
      {
        key: "regulatoryUrgency",
        label: "Priorità Cliente",
        weight: 20,
        definition: "1 = bassa urgenza o segmento piccolo. 5 = segmento ad alto valore, momento del journey visibile o rischio di insoddisfazione ricorrente."
      },
      {
        key: "dataComplexity",
        label: "Complessità Dati",
        weight: 15,
        definition: "1 = fonte semplice e campi puliti. 5 = feedback multi-fonte, CRM, service, dealer e contesto digitale."
      },
      {
        key: "stakeholderClarity",
        label: "Chiarezza Responsabile",
        weight: 15,
        definition: "1 = nessun responsabile business chiaro. 5 = responsabile CX, CRM, service, dealer o product chiaro."
      },
      {
        key: "deploymentFit",
        label: "Fit Reporting",
        weight: 10,
        definition: "1 = basso valore di reporting. 5 = forte fit per dashboard, segmentazione e revisione ricorrente dei trend."
      },
      {
        key: "procurementFeasibility",
        label: "Actionability",
        weight: 10,
        definition: "1 = prossima azione poco chiara. 5 = responsabile di miglioramento, percorso azione e metrica di follow-up realistici."
      }
    ]
  };

  d.pipelineStages = [
    { name: "Fonte Dati Identificata", probability: 0.10 },
    { name: "Dati Puliti", probability: 0.20 },
    { name: "Analisi Segmento", probability: 0.35 },
    { name: "Reporting Soddisfazione", probability: 0.50 },
    { name: "Diagnosi Journey", probability: 0.65 },
    { name: "Backlog Miglioramenti", probability: 0.75 },
    { name: "Action Pilot", probability: 0.85 },
    { name: "Azione Completata", probability: 1.00 },
    { name: "Handoff CX", probability: 1.00 }
  ];

  d.accounts = [
    {
      id: 1,
      company: "Onboarding nuovi proprietari Ducati",
      type: "Segmento cliente simulato",
      sector: "Onboarding proprietari",
      useCasePotential: "Analisi soddisfazione primi 30 giorni, feedback consegna e rilevazione frizioni onboarding",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "Customer Experience, CRM, dealer operations",
      reason: "Il primo periodo da proprietario influenza la loyalty di lungo periodo e offre una finestra chiara per misurare soddisfazione e follow-up proattivo.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 5, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 2,
      company: "Clienti Touring Multistrada",
      type: "Segmento cliente simulato",
      sector: "Loyalty",
      useCasePotential: "Segmentare il feedback dei proprietari long-distance per bisogni service, accessori, community e supporto post-viaggio",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "CX, product marketing, after-sales",
      reason: "I clienti touring generano feedback ricco su utilizzo, service, accessori e touchpoint della brand community.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 4, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 3,
      company: "Proprietari Panigale Performance",
      type: "Segmento cliente simulato",
      sector: "Premium Owners",
      useCasePotential: "Analizzare soddisfazione, aspettative, bisogni di supporto tecnico ed esperienza post-consegna dei proprietari premium",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "CX, product, dealer network",
      reason: "I clienti premium hanno alto valore e si aspettano supporto preciso, reattivo e tecnicamente credibile.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 4,
      company: "Rider Scrambler alla Prima Esperienza",
      type: "Segmento cliente simulato",
      sector: "Onboarding proprietari",
      useCasePotential: "Profilare bisogni dei nuovi rider, contenuti per costruire confidenza, educazione dealer e domande delle prime fasi da proprietario",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "CRM, CX, training, dealer operations",
      reason: "I rider più nuovi possono aver bisogno di onboarding più chiaro, contenuti di supporto e comunicazione personalizzata post-acquisto.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 5 }
    },
    {
      id: 5,
      company: "Journey Appuntamento Service",
      type: "Customer journey simulato",
      sector: "Service",
      useCasePotential: "Identificare frizioni in booking, reminder, tempo di attesa, spiegazione service e soddisfazione post-service",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "After-sales, dealer operations, CX",
      reason: "Le interazioni service sono frequenti, misurabili e fortemente collegate a loyalty ricorrente e percezione dealer.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 5, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 6,
      company: "Journey Reclamo Garanzia",
      type: "Customer journey simulato",
      sector: "Service",
      useCasePotential: "Analizzare temi di reclamo, tempi di risoluzione, chiarezza comunicativa e sentiment cliente dopo i claim",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "After-sales, legal/privacy, dealer operations",
      reason: "Le esperienze di garanzia possono creare insoddisfazione se comunicazione, timing o responsabilità non sono chiari.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 7,
      company: "Lead Configuratore Digitale",
      type: "Segmento cliente simulato",
      sector: "Digital",
      useCasePotential: "Collegare comportamento nel configuratore a richieste test ride, qualità lead, drop-off e timing follow-up",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "Digital, CRM, sales operations",
      reason: "Il comportamento digitale può indicare intenzione, ma richiede organizzazione accurata prima di diventare utile per team CX e CRM.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 8,
      company: "Partecipanti Test Ride",
      type: "Segmento cliente simulato",
      sector: "Events",
      useCasePotential: "Misurare soddisfazione post-evento, qualità follow-up, blocchi alla conversione e percezione brand",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "Events, CRM, dealer network",
      reason: "I test ride sono un momento chiaro per raccogliere aspettative, obiezioni e qualità del follow-up.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 5 }
    },
    {
      id: 9,
      company: "Utenti App e Connected Services",
      type: "Segmento cliente simulato",
      sector: "Digital",
      useCasePotential: "Analizzare feedback app, uso funzionalita, richieste supporto e trend di soddisfazione digitale",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "Digital product, CX, data/IT",
      reason: "I servizi digitali generano segnali ricorrenti traducibili in miglioramenti product e support.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 10,
      company: "Esperienza Follow-up Dealer",
      type: "Customer journey simulato",
      sector: "Dealer Network",
      useCasePotential: "Confrontare timing del follow-up, qualità risposta e soddisfazione cliente dopo richiesta o consegna",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "Dealer operations, CRM, CX",
      reason: "La qualità del follow-up è altamente azionabile e può essere rivista senza un sistema tecnico complesso.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 3, stakeholderClarity: 5, deploymentFit: 4, procurementFeasibility: 5 }
    },
    {
      id: 11,
      company: "Clienti Accessori e Apparel",
      type: "Segmento cliente simulato",
      sector: "Retail",
      useCasePotential: "Analizzare pattern di acquisto accessori, soddisfazione sulla disponibilità e supporto post-acquisto",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "Retail, e-commerce, CRM",
      reason: "I touchpoint retail creano segnali utili su loyalty, personalizzazione e aspettative di servizio.",
      scoreComponents: { useCaseValue: 3, regulatoryUrgency: 3, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 3, procurementFeasibility: 5 }
    },
    {
      id: 12,
      company: "Clienti Service Inattivi",
      type: "Segmento cliente simulato",
      sector: "Retention",
      useCasePotential: "Profilare clienti che smettono di usare canali service ufficiali e identificare opportunità di retention",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "After-sales, CRM, dealer network",
      reason: "Il comportamento service inattivo può segnalare gap di soddisfazione, dubbi sul prezzo, problemi di comodita o follow-up debole.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 13,
      company: "Prospect Usato e Trade-In",
      type: "Segmento cliente simulato",
      sector: "Retail",
      useCasePotential: "Analizzare driver decisionali, domande su finanziamento, tempi di risposta dealer e soddisfazione per tipo prospect",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Medio",
      decisionMakers: "Retail, CRM, dealer network",
      reason: "Percorsi trade-in e usato includono molteplici punti decisionali e possono beneficiare di profilazione più chiara.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 3, dataComplexity: 4, stakeholderClarity: 3, deploymentFit: 4, procurementFeasibility: 4 }
    },
    {
      id: 14,
      company: "Proprietari VIP e ricorrenti",
      type: "Segmento cliente simulato",
      sector: "Premium Owners",
      useCasePotential: "Monitorare driver di loyalty, soddisfazione eventi, servizi esclusivi e aspettative dei proprietari ad alto valore",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "CX, brand, CRM, events",
      reason: "I proprietari ricorrenti e premium sono preziosi per loyalty, advocacy e percezione brand.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 15,
      company: "Visitatori e Turisti Internazionali",
      type: "Segmento cliente simulato",
      sector: "Events",
      useCasePotential: "Profilare soddisfazione dei visitatori di museo, factory o eventi e bisogni di lingua/supporto",
      regulatorySensitivity: "Basso",
      dataComplexityLabel: "Medio",
      decisionMakers: "Events, customer care, brand experience",
      reason: "I visitatori internazionali possono rivelare opportunità di miglioramento su servizio, lingua e brand experience.",
      scoreComponents: { useCaseValue: 3, regulatoryUrgency: 3, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 3, procurementFeasibility: 4 }
    },
    {
      id: 16,
      company: "Detractor Post-Consegna",
      type: "Segmento cliente simulato",
      sector: "Onboarding proprietari",
      useCasePotential: "Rilevare temi low-NPS ricorrenti dopo la consegna e assegnare azioni di recovery",
      regulatorySensitivity: "Medio",
      dataComplexityLabel: "Alto",
      decisionMakers: "CX, dealer operations, CRM, privacy",
      reason: "I segnali detractor iniziali sono prioritari perche impattano soddisfazione, loyalty, referral e fiducia nel brand.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    }
  ];

  d.pipelineDeals = [
    { id: "CX1", accountId: 1, stage: "Reporting Soddisfazione", value: 42000, daysInStage: 8, pocReadiness: 74, risk: "Campione", nextStep: "Validare copertura survey primi 30 giorni e aggiungere note consegna dealer." },
    { id: "CX2", accountId: 2, stage: "Diagnosi Journey", value: 36000, daysInStage: 12, pocReadiness: 68, risk: "Collegamento dati", nextStep: "Collegare feedback service con note del segmento touring-use." },
    { id: "CX3", accountId: 3, stage: "Analisi Segmento", value: 18000, daysInStage: 6, pocReadiness: 54, risk: "Gap aspettative", nextStep: "Separare feedback di consegna da richieste di product support." },
    { id: "CX4", accountId: 4, stage: "Backlog Miglioramenti", value: 28000, daysInStage: 5, pocReadiness: 71, risk: "Responsabilità contenuti", nextStep: "Assegnare responsabile contenuti onboarding e definire metrica di follow-up." },
    { id: "CX5", accountId: 5, stage: "Action Pilot", value: 61000, daysInStage: 16, pocReadiness: 82, risk: "Processo dealer", nextStep: "Testare reminder appuntamento e template di spiegazione post-service." },
    { id: "CX6", accountId: 6, stage: "Diagnosi Journey", value: 24000, daysInStage: 18, pocReadiness: 63, risk: "Timing risoluzione", nextStep: "Mappare campi stato claim e gap comunicativi ricorrenti." },
    { id: "CX7", accountId: 7, stage: "Dati Puliti", value: 52000, daysInStage: 9, pocReadiness: 46, risk: "Attribuzione", nextStep: "Definire percorso evento da configuratore a follow-up lead." },
    { id: "CX8", accountId: 8, stage: "Azione Completata", value: 17000, daysInStage: 2, pocReadiness: 91, risk: "Nessuno", nextStep: "Confrontare soddisfazione del follow-up post-evento dopo il pilot." },
    { id: "CX9", accountId: 9, stage: "Reporting Soddisfazione", value: 31000, daysInStage: 10, pocReadiness: 69, risk: "Qualità fonte digitale", nextStep: "Separare ticket di supporto da feedback funzionalita." },
    { id: "CX10", accountId: 10, stage: "Backlog Miglioramenti", value: 47000, daysInStage: 7, pocReadiness: 77, risk: "Allineamento responsabile", nextStep: "Assegnare responsabile follow-up dealer e metrica target sul tempo di risposta." },
    { id: "CX11", accountId: 11, stage: "Fonte Dati Identificata", value: 14000, daysInStage: 4, pocReadiness: 31, risk: "Basso priority", nextStep: "Confermare quale touchpoint retail ha campione sufficiente." },
    { id: "CX12", accountId: 12, stage: "Diagnosi Journey", value: 33000, daysInStage: 14, pocReadiness: 61, risk: "Logica retention", nextStep: "Controllare completezza service history prima delle conclusioni di segmento." },
    { id: "CX13", accountId: 13, stage: "Analisi Segmento", value: 21000, daysInStage: 11, pocReadiness: 57, risk: "Chiarezza follow-up", nextStep: "Mappare domande su finanziamento e trade-in per tempo risposta dealer." },
    { id: "CX14", accountId: 14, stage: "Reporting Soddisfazione", value: 19000, daysInStage: 6, pocReadiness: 73, risk: "Campione piccolo", nextStep: "Usare note qualitative insieme ai segnali quantitativi di trend." },
    { id: "CX15", accountId: 15, stage: "Dati Puliti", value: 12000, daysInStage: 5, pocReadiness: 42, risk: "Campi lingua", nextStep: "Taggare campi lingua e tipo visita prima dell'analisi." },
    { id: "CX16", accountId: 16, stage: "Action Pilot", value: 26000, daysInStage: 13, pocReadiness: 84, risk: "Responsabilità recovery", nextStep: "Creare regola di contatto recovery e controllo soddisfazione post-azione." }
  ];

  d.executiveInsights = [
    {
      title: "Il feedback sul journey service ha il percorso d'azione più chiaro",
      signal: "I segmenti appuntamento service e garanzia combinano alto impatto sulla soddisfazione, alta complessità dati e responsabili after-sales nominati.",
      risk: "Se il feedback service resta frammentato, problemi ricorrenti possono essere visibili nei commenti ma non convertiti in azioni di miglioramento.",
      action: "Creare una vista service journey con campi booking, reminder, tempo di attesa, spiegazione e soddisfazione post-service.",
      impact: "Impatto atteso: prioritizzazione più chiara dei miglioramenti after-sales e assegnazione del responsabile più rapida."
    },
    {
      title: "Il comportamento digitale richiede una mappatura fonti più solida",
      signal: "I segmenti configuratore, app e connected services hanno alto valore di reporting ma dipendono da linkage dati e chiarezza delle fonti.",
      risk: "I team possono confondere segnali di interesse, bisogni di supporto e feedback di soddisfazione se la tassonomia fonti e debole.",
      action: "Separare comportamento lead, ticket supporto, feedback funzionalita e campi survey di soddisfazione prima del trend reporting.",
      impact: "Impatto atteso: segmentazione più affidabile e logica di follow-up CRM più chiara."
    },
    {
      title: "La fase iniziale da proprietario è una finestra feedback ad alta priorità",
      signal: "I segmenti onboarding nuovi proprietari e detractor post-consegna mostrano alto impatto sulla soddisfazione e forte actionability.",
      risk: "Se l insoddisfazione iniziale viene rilevata tardi, le azioni di recovery possono perdere il momento in cui la percezione cliente si sta ancora formando.",
      action: "Aggiungere una vista proprietari primi 30 giorni con feedback consegna, domande onboarding, follow-up dealer e stato recovery.",
      impact: "Impatto atteso: segnali retention più forti e azioni di customer recovery più tempestive."
    }
  ];

  d.bottlenecks = [
    {
      stage: "Mappatura Fonti Dati",
      signal: "Il feedback esiste su survey, CRM, note service, follow-up dealer e touchpoint digitali.",
      cause: "I segnali cliente sono raccolti in sistemi diversi e possono usare etichette o timing incoerenti.",
      action: "Creare una mappa fonti con responsabile fonte, cadenza refresh, qualità campo e stage del customer journey.",
      impact: "Migliorare l'affidabilità del reporting prima di trarre conclusioni sui segmenti."
    },
    {
      stage: "Diagnosi Journey",
      signal: "I segmenti prioritari spesso richiedono sia segnali quantitativi da survey sia temi qualitativi dai commenti.",
      cause: "Gli score da soli non spiegano se il problema riguarda timing, comunicazione, product support o processo dealer.",
      action: "Affiancare alle metriche dashboard note insight strutturate e una sintesi temi revisionata da una persona.",
      impact: "Rendere le evidenze più facili da comunicare e trasformare in azioni."
    },
    {
      stage: "Follow-up Azioni",
      signal: "La qualità degli insight conta solo se responsabilità e misurazione post-azione sono chiare.",
      cause: "I report possono essere rivisti senza un responsabile azione o una metrica target nominati.",
      action: "Usare una checklist di handoff azione con responsabile, scadenza, cambiamento metrica atteso e prossima data di revisione.",
      impact: "Chiudere il ciclo tra analytics e miglioramento customer experience."
    }
  ];

  d.stageExitCriteria = [
    {
      transition: "Fonte Dati Identificata -> Dati Puliti",
      criteria: [
        "Responsabile fonte identificato.",
        "Cadenza refresh nota.",
        "Stage customer journey rilevante mappato.",
        "Confini dei dati personali compresi.",
        "Campi mancanti o incoerenti registrati."
      ]
    },
    {
      transition: "Dati Puliti -> Analisi Segmento",
      criteria: [
        "Campione minimo controllato.",
        "Definizione segmento documentata.",
        "Valori mancanti e duplicati gestiti.",
        "Bias survey o feedback annotato.",
        "Prima domanda di analisi esplicita."
      ]
    },
    {
      transition: "Analisi Segmento -> Reporting Soddisfazione",
      criteria: [
        "Trend soddisfazione calcolato.",
        "Ipotesi driver primario documentata.",
        "Segmento di confronto o baseline disponibile.",
        "Limiti scritti in linguaggio chiaro.",
        "Responsabile reporting assegnato."
      ]
    },
    {
      transition: "Diagnosi Journey -> Backlog Miglioramenti",
      criteria: [
        "Ipotesi root-cause revisionata da un responsabile umano.",
        "Touchpoint impattato chiaro.",
        "Responsabile business nominato.",
        "Metrica cliente o operativa attesa selezionata.",
        "Domande privacy o uso dati risolte."
      ]
    },
    {
      transition: "Action Pilot -> Handoff CX",
      criteria: [
        "Responsabile azione e timeline confermati.",
        "Metrica target e baseline registrate.",
        "Data reporting follow-up pianificata.",
        "Gli stakeholder sanno quali evidenze saranno riviste.",
        "Le lezioni apprese saranno aggiunte al backlog."
      ]
    }
  ];

  d.handoffChecklist = [
    { title: "Segmento cliente definito chiaramente", desc: "Segmento, stage del journey e dati fonte sono documentati." },
    { title: "Segnale di soddisfazione validato", desc: "Campione, dati mancanti e direzione del trend sono controllati prima di condividere conclusioni." },
    { title: "Ipotesi driver primario scritta", desc: "La causa probabile è dichiarata chiaramente e separata dai fatti confermati." },
    { title: "Responsabile business nominato", desc: "Viene assegnato un responsabile CX, CRM, service, dealer, product o digital." },
    { title: "Metrica azione selezionata", desc: "Il miglioramento ha una metrica di follow-up misurabile, non solo un obiettivo qualitativo." },
    { title: "Confine uso dati controllato", desc: "Dati personali, aggregazione e responsabilità di accesso sono chiari." },
    { title: "Cadenza follow-up pianificata", desc: "La prossima data di revisione e la fonte evidenza sono documentate." },
    { title: "Apprendimento registrato", desc: "I risultati rientrano nel modello segmenti o nel backlog reporting." }
  ];

  d.complianceChecklist = [
    "L'analisi coinvolge dati personali cliente o note dealer/cliente identificabili?",
    "L'evidenza può essere riportata a livello aggregato o segmento invece che individuale?",
    "Il campione è abbastanza ampio per supportare una conclusione dashboard?",
    "Bias survey, valori mancanti, duplicati o campi non aggiornati sono documentati?",
    "Un responsabile umano sta revisionando ogni bozza di sintesi insight cliente prima dell'uso?",
    "Chi possiede l approvazione tra CX, CRM, Data/IT, Privacy e business stakeholder?"
  ];
  d.complianceEscalationRule = "Regola di escalation: se emergono uso di dati personali, aggregazione poco chiara o responsabilità fonte sconosciuta, segnalare per revisione Data/IT o Privacy prima di usare la fonte nel reporting.";

  d.sectorBuyingDrivers = {
    "Onboarding proprietari": "soddisfazione primi 30 giorni, chiarezza consegna, follow-up dealer, contenuti onboarding e azioni early recovery",
    "Loyalty": "relazione ricorrente, esperienza service, engagement community, accessori e soddisfazione lungo periodo",
    "Premium Owners": "aspettative alte, credibilita tecnica, reattività, esperienza esclusiva e fiducia nel brand",
    "Service": "facilità booking, chiarezza comunicativa, tempo di attesa, spiegazione riparazione e soddisfazione post-service",
    "Digital": "usabilita app, comportamento configuratore, supporto digitale, qualità lead e feedback funzionalita",
    "Events": "soddisfazione test ride, visitor experience, qualità follow-up, supporto lingua e percezione brand",
    "Dealer Network": "tempo risposta, coerenza follow-up, qualità consegna e miglioramento processo frontline",
    "Retail": "disponibilità, supporto post-acquisto, segnali cross-sell e soddisfazione per tipo acquisto",
    "Retention": "motivi di abbandono service, comodita, percezione prezzo, qualità relazione e opportunità di riattivazione"
  };

  d.briefPromptStructure = [
    "Contesto segmento cliente",
    "Touchpoint journey rilevanti",
    "Segnale primario di soddisfazione o comportamento",
    "Fonti dati probabili",
    "Domande su qualità dati e privacy",
    "Ipotesi trend o frizione",
    "Prossima azione CX raccomandata",
    "Note handoff azione"
  ];

  d.methodologySections = [
    {
      title: "Cosa e simulato",
      items: [
        "Segmenti cliente, volumi feedback, stage del journey, segnali trend, action readiness e componenti score.",
        "Gli score sono illustrativi e progettati per mostrare logica di prioritizzazione, non giudizi fattuali su clienti, dealer o prodotti Ducati.",
        "I brief insight sono generati da dati strutturati predefiniti e assunzioni simulate di Customer Experience."
      ]
    },
    {
      title: "Cosa si basa su assunzioni rilevanti per il ruolo",
      items: [
        "Il tirocinio richiede raccolta, organizzazione, analisi, reporting, segmentazione e comunicazione chiara.",
        "I team Customer Experience lavorano comunemente con survey, CRM, service, dealer, digital e feedback di campagna.",
        "La customer analytics responsabile richiede attenzione a privacy, aggregazione, qualità delle fonti e interpretazione accurata."
      ]
    },
    {
      title: "Cosa dimostra il progetto",
      items: [
        "Ragionamento su workflow dati cliente e criteri di stage espliciti.",
        "Prioritizzazione segmenti tramite framework di scoring ponderato.",
        "Logica dashboard basata su volume insight totale e ponderato.",
        "Diagnostica trend: segnali, cause probabili, azioni e impatto atteso.",
        "Design handoff CX-to-business e qualificazione dati privacy-aware."
      ]
    },
    {
      title: "Cosa non è il progetto",
      items: [
        "Un sistema CX analytics di produzione, un'integrazione CRM o un deployment Power BI.",
        "Una rappresentazione di dati cliente Ducati riservati, survey interne o informazioni dealer.",
        "Un affermazione che Ducati usi o valuti questa soluzione specifica."
      ]
    }
  ];
})();
