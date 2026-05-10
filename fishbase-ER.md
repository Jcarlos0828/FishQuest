# FishBase ER Diagrams — cboettig/fishbase (v25.04)

[FishBase](https://www.fishbase.org) is the world's reference database on fishes. This repository consumes the `cboettig/fishbase` dataset on HuggingFace, which distributes 216 FishBase tables as individual Parquet files under `data/fb/v25.04/parquet/`.

This document describes the entity-relationship schema of that dataset, organized into 10 thematic domains.

---

## Schema Hub Keys

| Field | Owner table | Role |
|---|---|---|
| `SpecCode` | `species` | Central PK — unique species identifier, referenced by ~150 tables |
| `StockCode` | `stocks` | Stock PK — population subdivision of a species, referenced by ~80 tables |
| `FamCode` | `families` | Taxonomic family PK |
| `GenCode` | `genera` | Taxonomic genus PK |
| `Ordnum` | `orders` | Taxonomic order PK (`Order` field is text, not the numeric key) |
| `ClassNum` | `classes` | Taxonomic class PK |
| `C_Code` | `countref` | Country/region PK (ISO-like code) |
| `RefNo` | `refrens` | Bibliographic reference PK |
| `AreaCode` | `faoarref` | FAO area PK |
| `E_CODE` | `ecosystemref` | Ecosystem PK |
| `DietCode` | `diet` | Diet record PK (referenced by `diet_items`) |
| `LFCode` | `poplf` | Length-frequency distribution PK (referenced by `poplfdata`) |
| `FishCode` | `fl_fish` | PK within the Food Loss sub-dataset |
| `DisCode` | `disref` | Disease catalogue PK |
| `AqCode` | `aquariumref` | Aquarium directory PK |
| `OccurrenceRefNo` | `occurrence` | Occurrence semantic PK — referenced by `museum` and `collectionsref` |

---

## Reading Conventions

- Each diagram shows only **PK** and **FK** columns per table (not all columns).
- Hub entities (`species`, `stocks`, `refrens`, `countref`, etc.) are repeated across diagrams with only their PK for context.
- Cardinality `||--o{` = one-to-many.
- The label on each relationship is the name of the FK field in the source table.

---

### D1 — Core Taxonomy

```mermaid
erDiagram
    species {
        int SpecCode PK
        int FamCode FK
        int GenCode FK
        int SpeciesRefNo FK
    }
    genera {
        int GenCode PK
        int FamCode FK
        int GenRefno FK
    }
    families {
        int FamCode PK
        int Ordnum FK
        int ClassNum FK
        int FamiliesRefNo FK
    }
    orders {
        int Ordnum PK
        int ClassNum FK
        int OrderRefNo FK
        string Order
    }
    classes {
        int ClassNum PK
        int ClassRefNo FK
    }
    synonyms {
        int SynCode PK
        int SpecCode FK
        int SynonymsRef FK
    }
    allgenus {
        string Genus
        int FamCode FK
    }
    speciesauthorsnames {
        int SpecCode FK
        int SynCode FK
    }
    taxamatch {
        int SpecCode FK
        int SynCode FK
    }
    taxamatch_epithet {
        int SpecCode FK
        int SynCode FK
    }
    revisions {
        int FamCode FK
        int GenCode FK
        int RefNo FK
    }
    refrens {
        int RefNo PK
    }

    classes ||--o{ orders : "ClassNum"
    orders ||--o{ families : "Ordnum"
    families ||--o{ genera : "FamCode"
    families ||--o{ allgenus : "FamCode"
    genera ||--o{ species : "GenCode"
    species ||--o{ synonyms : "SpecCode"
    species ||--o{ speciesauthorsnames : "SpecCode"
    species ||--o{ taxamatch : "SpecCode"
    species ||--o{ taxamatch_epithet : "SpecCode"
    refrens ||--o{ species : "SpeciesRefNo"
    refrens ||--o{ revisions : "RefNo"
    families ||--o{ revisions : "FamCode"
    genera ||--o{ revisions : "GenCode"
```

---

### D2 — Common Names and Country References

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
        int SpecCode FK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
        int AreaCodeMarineI FK
    }
    families {
        int FamCode PK
    }
    orders {
        int Ordnum PK
    }
    comnames {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        string C_Code FK
        int ComNamesRefNo FK
    }
    country {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        string C_Code FK
        int CountryRefNo FK
    }
    countrysub {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        string C_Code FK
        int CSubRefNo FK
    }
    countrysubref {
        string CSub_Code PK
        string C_Code FK
    }
    countrysubfaoref {
        string C_Code FK
        string CSub_Code FK
    }
    language {
        string LangCode PK
        string C_Code FK
    }
    languagecountry {
        string LangCode FK
        string C_Code FK
        int RefNo FK
    }
    languagescript {
        string ScriptCode PK
        string C_Code FK
    }
    isscaap {
        int AutoCtr PK
        int SpecCode FK
        int StockCode FK
        int FamCode FK
        int OrdNum FK
        int RefNo FK
    }
    checklist {
        string C_Code FK
        int Refno FK
    }
    faoarref {
        int AreaCode PK
    }

    species ||--o{ stocks : "SpecCode"
    species ||--o{ comnames : "SpecCode"
    stocks ||--o{ comnames : "StockCode"
    countref ||--o{ comnames : "C_Code"
    refrens ||--o{ comnames : "ComNamesRefNo"
    species ||--o{ country : "SpecCode"
    stocks ||--o{ country : "StockCode"
    countref ||--o{ country : "C_Code"
    countref ||--o{ countrysub : "C_Code"
    countrysubref ||--o{ countrysub : "CSub_Code"
    countref ||--o{ countrysubref : "C_Code"
    countref ||--o{ countrysubfaoref : "C_Code"
    countref ||--o{ language : "C_Code"
    countref ||--o{ languagecountry : "C_Code"
    refrens ||--o{ languagecountry : "RefNo"
    countref ||--o{ languagescript : "C_Code"
    species ||--o{ isscaap : "SpecCode"
    stocks ||--o{ isscaap : "StockCode"
    families ||--o{ isscaap : "FamCode"
    orders ||--o{ isscaap : "OrdNum"
    refrens ||--o{ isscaap : "RefNo"
    countref ||--o{ checklist : "C_Code"
    faoarref ||--o{ countref : "AreaCodeMarineI"
```

---

### D3 — Geography and Distribution

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
        int SpecCode FK
        int StocksRefNo FK
    }
    faoarref {
        int AreaCode PK
    }
    countref {
        string C_Code PK
    }
    ecosystemref {
        int E_CODE PK
    }
    refrens {
        int RefNo PK
    }
    families {
        int FamCode PK
    }
    orders {
        int Ordnum PK
        string Order
    }
    faoareas {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        int AreaCode FK
    }
    faoarfam {
        int FamCode FK
        int AreaCode FK
    }
    faoarord {
        string Order FK
        int AreaCode FK
    }
    faocatch {
        int autoctr PK
        string C_Code FK
        int AreaCode FK
    }
    faoaquacult {
        int autoctr PK
        string C_Code FK
        int AreaCode FK
    }
    icescatch {
        int AutoCtr PK
        string C_Code FK
    }
    countfao {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        string C_Code FK
        int AreaCode FK
    }
    countfaoref {
        string C_Code FK
        int AreaCode FK
    }
    occurrence {
        int OccurrenceRefNo PK
        int SpecCode FK
        int Stockcode FK
        string C_Code FK
    }
    intrcase {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        int IntrCaseRefNo FK
        string C_Code_To FK
    }
    ecosystem {
        int autoctr PK
        int E_CODE FK
        int Speccode FK
        int Stockcode FK
        int EcosystemRefno FK
    }
    ecosystemcountry {
        int autoctr PK
        int E_CODE FK
        string C_Code FK
        int Speccode FK
        int Stockcode FK
    }
    countecosystem {
        int autoctr PK
        int E_CODE FK
        string C_Code FK
        int Speccode FK
    }
    ecosysfam {
        int E_CODE FK
        int FamCode FK
    }
    ecosystemfaoref {
        int E_CODE FK
        int AreaCode FK
    }
    ecosystemcntref {
        int E_CODE FK
        string C_CODE FK
    }
    ecosyslhref {
        int E_CODE FK
    }
    oceanprovinces {
        int StockCode FK
        int SpecCode FK
        int ProvinceRef FK
    }
    oceanprovfaoref {
        int AreaCode FK
        int RegionNo
    }
    gazetteer {
        int GazetCode PK
        string C_CODE FK
        int AreaCodeMarine FK
    }
    bruvssurvey {
        int ExpeditionID PK
        string C_Code FK
        int E_Code FK
        int AreaCode FK
    }
    bruvssample {
        int SampleID PK
        int ExpeditionID FK
    }
    bruvsspecies {
        int RecordID PK
        int SampleID FK
        int FamCode FK
        int Speccode FK
    }

    species ||--o{ stocks : "SpecCode"
    species ||--o{ faoareas : "SpecCode"
    stocks ||--o{ faoareas : "StockCode"
    faoarref ||--o{ faoareas : "AreaCode"
    families ||--o{ faoarfam : "FamCode"
    faoarref ||--o{ faoarfam : "AreaCode"
    orders ||--o{ faoarord : "Order"
    faoarref ||--o{ faoarord : "AreaCode"
    countref ||--o{ faocatch : "C_Code"
    faoarref ||--o{ faocatch : "AreaCode"
    countref ||--o{ faoaquacult : "C_Code"
    faoarref ||--o{ faoaquacult : "AreaCode"
    countref ||--o{ icescatch : "C_Code"
    species ||--o{ countfao : "SpecCode"
    stocks ||--o{ countfao : "StockCode"
    countref ||--o{ countfao : "C_Code"
    faoarref ||--o{ countfao : "AreaCode"
    countref ||--o{ countfaoref : "C_Code"
    faoarref ||--o{ countfaoref : "AreaCode"
    species ||--o{ occurrence : "SpecCode"
    stocks ||--o{ occurrence : "Stockcode"
    countref ||--o{ occurrence : "C_Code"
    species ||--o{ intrcase : "SpecCode"
    stocks ||--o{ intrcase : "StockCode"
    refrens ||--o{ intrcase : "IntrCaseRefNo"
    countref ||--o{ intrcase : "C_Code_To"
    ecosystemref ||--o{ ecosystem : "E_CODE"
    species ||--o{ ecosystem : "Speccode"
    stocks ||--o{ ecosystem : "Stockcode"
    refrens ||--o{ ecosystem : "EcosystemRefno"
    ecosystemref ||--o{ ecosystemcountry : "E_CODE"
    countref ||--o{ ecosystemcountry : "C_Code"
    species ||--o{ ecosystemcountry : "Speccode"
    ecosystemref ||--o{ countecosystem : "E_CODE"
    countref ||--o{ countecosystem : "C_Code"
    species ||--o{ countecosystem : "Speccode"
    ecosystemref ||--o{ ecosysfam : "E_CODE"
    families ||--o{ ecosysfam : "FamCode"
    ecosystemref ||--o{ ecosystemfaoref : "E_CODE"
    faoarref ||--o{ ecosystemfaoref : "AreaCode"
    ecosystemref ||--o{ ecosystemcntref : "E_CODE"
    countref ||--o{ ecosystemcntref : "C_CODE"
    ecosystemref ||--o{ ecosyslhref : "E_CODE"
    stocks ||--o{ oceanprovinces : "StockCode"
    species ||--o{ oceanprovinces : "SpecCode"
    refrens ||--o{ oceanprovinces : "ProvinceRef"
    faoarref ||--o{ oceanprovfaoref : "AreaCode"
    countref ||--o{ gazetteer : "C_CODE"
    faoarref ||--o{ gazetteer : "AreaCodeMarine"
    countref ||--o{ bruvssurvey : "C_Code"
    ecosystemref ||--o{ bruvssurvey : "E_Code"
    faoarref ||--o{ bruvssurvey : "AreaCode"
    bruvssurvey ||--o{ bruvssample : "ExpeditionID"
    bruvssample ||--o{ bruvsspecies : "SampleID"
    families ||--o{ bruvsspecies : "FamCode"
    species ||--o{ bruvsspecies : "Speccode"
```

---

### D4 — Ecology and Feeding

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    ecosystemref {
        int E_CODE PK
    }
    ecology {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        int EcologyRefNo FK
    }
    diet {
        int DietCode PK
        int StockCode FK
        int Speccode FK
        int DietRefNo FK
        string C_Code FK
        int E_Code FK
    }
    diet_items {
        int autoctr PK
        int DietCode FK
        int DietSpeccode FK
    }
    fooditems {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        string C_Code FK
        int FoodsRefNo FK
        int PreySpecCode FK
    }
    food {
        int AutoCtr PK
        int Refno FK
    }
    foodtroph {
        int RefNo FK
    }
    predats {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        string C_Code FK
        int PredatsRefNo FK
    }
    ration {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int RDRefNo FK
        string C_Code FK
    }
    globi {
        int SpecCode FK
    }
    homerange {
        int HomeRangeID PK
        int Speccode FK
        int Stockcode FK
        int HomeRangeRefno FK
    }
    gomexsi {
        int speccode FK
    }
    alieninvasive {
        int Autoctr PK
        int Speccode FK
    }
    aquamaps {
        int speccode FK
    }

    species ||--o{ ecology : "SpecCode"
    stocks ||--o{ ecology : "StockCode"
    refrens ||--o{ ecology : "EcologyRefNo"
    species ||--o{ diet : "Speccode"
    stocks ||--o{ diet : "StockCode"
    refrens ||--o{ diet : "DietRefNo"
    countref ||--o{ diet : "C_Code"
    ecosystemref ||--o{ diet : "E_Code"
    diet ||--o{ diet_items : "DietCode"
    species ||--o{ diet_items : "DietSpeccode"
    species ||--o{ fooditems : "SpecCode"
    stocks ||--o{ fooditems : "StockCode"
    countref ||--o{ fooditems : "C_Code"
    refrens ||--o{ fooditems : "FoodsRefNo"
    species ||--o{ fooditems : "PreySpecCode"
    refrens ||--o{ food : "Refno"
    refrens ||--o{ foodtroph : "RefNo"
    species ||--o{ predats : "SpecCode"
    stocks ||--o{ predats : "StockCode"
    countref ||--o{ predats : "C_Code"
    refrens ||--o{ predats : "PredatsRefNo"
    species ||--o{ ration : "SpecCode"
    stocks ||--o{ ration : "StockCode"
    refrens ||--o{ ration : "RDRefNo"
    countref ||--o{ ration : "C_Code"
    species ||--o{ globi : "SpecCode"
    species ||--o{ homerange : "Speccode"
    stocks ||--o{ homerange : "Stockcode"
    refrens ||--o{ homerange : "HomeRangeRefno"
    species ||--o{ gomexsi : "speccode"
    species ||--o{ alieninvasive : "Speccode"
    species ||--o{ aquamaps : "speccode"
```

---

### D5 — Population Dynamics

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    ecosystemref {
        int E_CODE PK
    }
    families {
        int FamCode PK
    }
    popgrowth {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int E_CODE FK
        int PopGrowthRef FK
        string C_Code FK
    }
    popchar {
        int Autoctr PK
        int Speccode FK
        int Stockcode FK
        int PopCharRefNo FK
        string C_Code FK
    }
    poplw {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int FamCode FK
        int PopLWRef FK
        string C_Code FK
    }
    poplf {
        int LFCode PK
        int Stockcode FK
        int Speccode FK
        int LFRefno FK
        string C_Code FK
    }
    poplfdata {
        int autoctr PK
        int LFCode FK
    }
    popll {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
    }
    popqb {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int PopQBRefNo FK
        string C_Code FK
    }
    pop_r {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int POP_r_Ref FK
    }
    pop_rm {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int PopRMRef FK
    }
    popular {
        int Speccode FK
    }
    estimate {
        int SpecCode FK
    }
    matrix {
        int ID PK
        int SpecCode FK
        int FamCode FK
        int stockcode FK
    }

    species ||--o{ popgrowth : "SpecCode"
    stocks ||--o{ popgrowth : "StockCode"
    ecosystemref ||--o{ popgrowth : "E_CODE"
    refrens ||--o{ popgrowth : "PopGrowthRef"
    countref ||--o{ popgrowth : "C_Code"
    species ||--o{ popchar : "Speccode"
    stocks ||--o{ popchar : "Stockcode"
    refrens ||--o{ popchar : "PopCharRefNo"
    countref ||--o{ popchar : "C_Code"
    species ||--o{ poplw : "SpecCode"
    stocks ||--o{ poplw : "StockCode"
    families ||--o{ poplw : "FamCode"
    refrens ||--o{ poplw : "PopLWRef"
    countref ||--o{ poplw : "C_Code"
    species ||--o{ poplf : "Speccode"
    stocks ||--o{ poplf : "Stockcode"
    refrens ||--o{ poplf : "LFRefno"
    countref ||--o{ poplf : "C_Code"
    poplf ||--o{ poplfdata : "LFCode"
    species ||--o{ popll : "SpecCode"
    stocks ||--o{ popll : "StockCode"
    species ||--o{ popqb : "SpecCode"
    stocks ||--o{ popqb : "StockCode"
    refrens ||--o{ popqb : "PopQBRefNo"
    countref ||--o{ popqb : "C_Code"
    species ||--o{ pop_r : "SpecCode"
    stocks ||--o{ pop_r : "StockCode"
    refrens ||--o{ pop_r : "POP_r_Ref"
    species ||--o{ pop_rm : "SpecCode"
    stocks ||--o{ pop_rm : "StockCode"
    refrens ||--o{ pop_rm : "PopRMRef"
    species ||--o{ popular : "Speccode"
    species ||--o{ estimate : "SpecCode"
    species ||--o{ matrix : "SpecCode"
    families ||--o{ matrix : "FamCode"
    stocks ||--o{ matrix : "stockcode"
```

---

### D6 — Morphology, Physiology and Reproduction

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    ecosystemref {
        int E_CODE PK
    }
    families {
        int FamCode PK
    }
    morphdat {
        int autoctr PK
        int Speccode FK
        int StockCode FK
        int MorphDatRefNo FK
    }
    morphmet {
        int autoctr PK
        int Speccode FK
    }
    morphmettlratios {
        int Speccode FK
        int FamCode FK
        int ClassNum FK
    }
    maturity {
        int autoctr PK
        int Speccode FK
        int StockCode FK
        int MaturityRefNo FK
        string C_Code FK
        int E_CODE FK
    }
    maturitygills {
        int SpecCode FK
        int StockCode FK
    }
    spawning {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int SpawningRefNo FK
        string C_Code FK
        int E_CODE FK
    }
    spawnagg {
        int SpawnAggID PK
        int SpecCode FK
        string C_Code FK
        int SpawnAggRef FK
    }
    fecundity {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int MainRefNo FK
        string C_Code FK
        int E_CODE FK
    }
    reproduc {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int ReproducRefNo FK
        int MatingRefNo FK
    }
    eggdev {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int EggDevRefNo FK
        string C_Code FK
    }
    eggs {
        int Stockcode FK
        int Speccode FK
        int EggsRefNo FK
    }
    gillarea {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int GillAreaRefNo FK
    }
    otoliths {
        int OtolithID PK
        int SpecCode FK
        string C_Code FK
        int E_CODE FK
        int OtolithsRefno FK
    }
    vision {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int VisionRefNo FK
    }
    massconversion {
        int RecordNo PK
        int Speccode FK
        int StockCode FK
        int MassConvRefNo FK
    }
    elecstudies {
        int StockCode FK
        int SpecCode FK
        int ElecDatRefNo FK
        string C_Code FK
    }

    species ||--o{ morphdat : "Speccode"
    stocks ||--o{ morphdat : "StockCode"
    refrens ||--o{ morphdat : "MorphDatRefNo"
    species ||--o{ morphmet : "Speccode"
    species ||--o{ morphmettlratios : "Speccode"
    families ||--o{ morphmettlratios : "FamCode"
    species ||--o{ maturity : "Speccode"
    stocks ||--o{ maturity : "StockCode"
    refrens ||--o{ maturity : "MaturityRefNo"
    countref ||--o{ maturity : "C_Code"
    ecosystemref ||--o{ maturity : "E_CODE"
    species ||--o{ maturitygills : "SpecCode"
    stocks ||--o{ maturitygills : "StockCode"
    species ||--o{ spawning : "SpecCode"
    stocks ||--o{ spawning : "StockCode"
    refrens ||--o{ spawning : "SpawningRefNo"
    countref ||--o{ spawning : "C_Code"
    ecosystemref ||--o{ spawning : "E_CODE"
    species ||--o{ spawnagg : "SpecCode"
    countref ||--o{ spawnagg : "C_Code"
    refrens ||--o{ spawnagg : "SpawnAggRef"
    species ||--o{ fecundity : "SpecCode"
    stocks ||--o{ fecundity : "StockCode"
    refrens ||--o{ fecundity : "MainRefNo"
    countref ||--o{ fecundity : "C_Code"
    ecosystemref ||--o{ fecundity : "E_CODE"
    species ||--o{ reproduc : "SpecCode"
    stocks ||--o{ reproduc : "StockCode"
    refrens ||--o{ reproduc : "ReproducRefNo"
    species ||--o{ eggdev : "SpecCode"
    stocks ||--o{ eggdev : "StockCode"
    refrens ||--o{ eggdev : "EggDevRefNo"
    countref ||--o{ eggdev : "C_Code"
    species ||--o{ eggs : "Speccode"
    stocks ||--o{ eggs : "Stockcode"
    refrens ||--o{ eggs : "EggsRefNo"
    species ||--o{ gillarea : "SpecCode"
    stocks ||--o{ gillarea : "StockCode"
    refrens ||--o{ gillarea : "GillAreaRefNo"
    species ||--o{ otoliths : "SpecCode"
    countref ||--o{ otoliths : "C_Code"
    ecosystemref ||--o{ otoliths : "E_CODE"
    refrens ||--o{ otoliths : "OtolithsRefno"
    species ||--o{ vision : "SpecCode"
    stocks ||--o{ vision : "StockCode"
    refrens ||--o{ vision : "VisionRefNo"
    species ||--o{ massconversion : "Speccode"
    stocks ||--o{ massconversion : "StockCode"
    refrens ||--o{ massconversion : "MassConvRefNo"
    species ||--o{ elecstudies : "SpecCode"
    stocks ||--o{ elecstudies : "StockCode"
    refrens ||--o{ elecstudies : "ElecDatRefNo"
    countref ||--o{ elecstudies : "C_Code"
```

---

### D7 — Environment, Aquaculture and Life Cycle

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    ecosystemref {
        int E_CODE PK
    }
    oxygen {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        int OxygenRefNo FK
    }
    waterquality {
        int autoctr PK
        int Speccode FK
    }
    speed {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int SpeedRefNo FK
    }
    swimming {
        int SpecCode FK
        int SwimRefMain FK
    }
    larvae {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int LarvaeRefNo FK
    }
    larvaepresence {
        int Autoctr PK
        int StockCode FK
        int SpecCode FK
        int LarvalRefNo FK
        string C_Code FK
    }
    larvalswimspeed {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int SpeedRefNo FK
        string C_Code FK
    }
    larvdyn {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int LarvDynRefNo FK
    }
    larvalnurserysystem {
        int autoctr PK
        int Speccode FK
        int Stockcode FK
        string C_Code FK
    }
    brains {
        int autoctr PK
        int SpecCode FK
        int StockCode FK
        int BRAINSRefNo FK
    }
    estimatedepth {
        int Speccode FK
    }
    broodstock {
        int autoctr PK
        int Speccode FK
        int Stockcode FK
        string C_Code FK
    }
    cultspec {
        int StockCode FK
        int SpecCode FK
        int CultSpecRefNo FK
    }
    cultures {
        int SpecCode FK
        int StockCode FK
    }
    cultsys {
        int StockCode FK
        int SpecCode FK
        int CultSysRefNo FK
        string C_Code FK
    }
    eggnurserysystem {
        int autoctr PK
        int Speccode FK
        int Stockcode FK
        string C_Code FK
    }
    frynurserysystem {
        int autoctr PK
        int Speccode FK
        int Stockcode FK
        string C_Code FK
    }
    aquamaint {
        int autoctr PK
        int SpecCode FK
    }
    aquarium {
        int AutoCtr PK
        int Stockcode FK
        int SpecCode FK
        int AqCode FK
    }
    aquariumref {
        int AqCode PK
        string C_code FK
    }
    proxims {
        int StockCode FK
        int SpecCode FK
        int ChemicsRefNo FK
        string C_Code FK
    }
    nutrientssummary {
        int Speccode FK
        int NutrientRefNo FK
    }
    abundance {
        int AbundanceCode PK
        int StockCode FK
        int SpecCode FK
        string C_Code FK
        int E_CODE FK
    }

    species ||--o{ oxygen : "SpecCode"
    stocks ||--o{ oxygen : "StockCode"
    refrens ||--o{ oxygen : "OxygenRefNo"
    species ||--o{ waterquality : "Speccode"
    species ||--o{ speed : "SpecCode"
    stocks ||--o{ speed : "StockCode"
    refrens ||--o{ speed : "SpeedRefNo"
    species ||--o{ swimming : "SpecCode"
    refrens ||--o{ swimming : "SwimRefMain"
    species ||--o{ larvae : "SpecCode"
    stocks ||--o{ larvae : "StockCode"
    refrens ||--o{ larvae : "LarvaeRefNo"
    species ||--o{ larvaepresence : "SpecCode"
    stocks ||--o{ larvaepresence : "StockCode"
    refrens ||--o{ larvaepresence : "LarvalRefNo"
    countref ||--o{ larvaepresence : "C_Code"
    species ||--o{ larvalswimspeed : "SpecCode"
    stocks ||--o{ larvalswimspeed : "StockCode"
    refrens ||--o{ larvalswimspeed : "SpeedRefNo"
    countref ||--o{ larvalswimspeed : "C_Code"
    species ||--o{ larvdyn : "SpecCode"
    stocks ||--o{ larvdyn : "StockCode"
    refrens ||--o{ larvdyn : "LarvDynRefNo"
    species ||--o{ larvalnurserysystem : "Speccode"
    stocks ||--o{ larvalnurserysystem : "Stockcode"
    countref ||--o{ larvalnurserysystem : "C_Code"
    species ||--o{ brains : "SpecCode"
    stocks ||--o{ brains : "StockCode"
    refrens ||--o{ brains : "BRAINSRefNo"
    species ||--o{ estimatedepth : "Speccode"
    species ||--o{ broodstock : "Speccode"
    stocks ||--o{ broodstock : "Stockcode"
    countref ||--o{ broodstock : "C_Code"
    species ||--o{ cultspec : "SpecCode"
    stocks ||--o{ cultspec : "StockCode"
    refrens ||--o{ cultspec : "CultSpecRefNo"
    species ||--o{ cultures : "SpecCode"
    stocks ||--o{ cultures : "StockCode"
    species ||--o{ cultsys : "SpecCode"
    stocks ||--o{ cultsys : "StockCode"
    refrens ||--o{ cultsys : "CultSysRefNo"
    countref ||--o{ cultsys : "C_Code"
    species ||--o{ eggnurserysystem : "Speccode"
    stocks ||--o{ eggnurserysystem : "Stockcode"
    countref ||--o{ eggnurserysystem : "C_Code"
    species ||--o{ frynurserysystem : "Speccode"
    stocks ||--o{ frynurserysystem : "Stockcode"
    countref ||--o{ frynurserysystem : "C_Code"
    species ||--o{ aquamaint : "SpecCode"
    species ||--o{ aquarium : "SpecCode"
    stocks ||--o{ aquarium : "Stockcode"
    aquariumref ||--o{ aquarium : "AqCode"
    countref ||--o{ aquariumref : "C_code"
    species ||--o{ proxims : "SpecCode"
    stocks ||--o{ proxims : "StockCode"
    refrens ||--o{ proxims : "ChemicsRefNo"
    countref ||--o{ proxims : "C_Code"
    species ||--o{ nutrientssummary : "Speccode"
    refrens ||--o{ nutrientssummary : "NutrientRefNo"
    species ||--o{ abundance : "SpecCode"
    stocks ||--o{ abundance : "StockCode"
    countref ||--o{ abundance : "C_Code"
    ecosystemref ||--o{ abundance : "E_CODE"
```

---

### D8 — Genetics, Health and Fisheries

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    ecosystemref {
        int E_CODE PK
    }
    families {
        int FamCode PK
    }
    genetics {
        int AutoCtr PK
        int StockCode FK
        int SpecCode FK
        int GeneticsRefNo FK
        string C_Code FK
    }
    genedat {
        int autoctr PK
        int StockCode FK
        int SpecCode FK
        int GeneDatRefNo FK
        string C_Code FK
    }
    gendiversity {
        int autoctr PK
        int speccode FK
        int e_code FK
        string c_code FK
    }
    strains {
        int StockCode FK
        int SpecCode FK
        int StrainsRefNo FK
        string C_Code FK
    }
    cigua {
        int AutoCtr PK
        int SpecCode FK
        int FamCode FK
        string C_Code FK
    }
    ciguafb {
        int AutoCtr PK
        int SpecCode FK
        string C_Code FK
    }
    disref {
        string DisCode PK
        int DiseasesRefNo FK
    }
    diseases {
        int StockCode FK
        int SpecCode FK
        int DiseasesRefNo FK
        string DisCode FK
        string C_Code FK
    }
    abnorm {
        int AutoCtr PK
        int SpecCode FK
        int StockCode FK
        int ABNORMRefNo FK
    }
    abnormref {
        int AutoCtr PK
        int RefNo FK
    }
    citesfb {
        int RefNo FK
    }
    seafoodad {
        int autoctr PK
        int Speccode FK
        string c_code_caught FK
    }
    seafoodadref {
        int GuideID PK
        string c_code_web FK
    }
    oceanadaptspecieslinks {
        int speccode FK
    }

    species ||--o{ genetics : "SpecCode"
    stocks ||--o{ genetics : "StockCode"
    refrens ||--o{ genetics : "GeneticsRefNo"
    countref ||--o{ genetics : "C_Code"
    species ||--o{ genedat : "SpecCode"
    stocks ||--o{ genedat : "StockCode"
    refrens ||--o{ genedat : "GeneDatRefNo"
    countref ||--o{ genedat : "C_Code"
    species ||--o{ gendiversity : "speccode"
    ecosystemref ||--o{ gendiversity : "e_code"
    countref ||--o{ gendiversity : "c_code"
    species ||--o{ strains : "SpecCode"
    stocks ||--o{ strains : "StockCode"
    refrens ||--o{ strains : "StrainsRefNo"
    countref ||--o{ strains : "C_Code"
    species ||--o{ cigua : "SpecCode"
    families ||--o{ cigua : "FamCode"
    countref ||--o{ cigua : "C_Code"
    species ||--o{ ciguafb : "SpecCode"
    countref ||--o{ ciguafb : "C_Code"
    species ||--o{ diseases : "SpecCode"
    stocks ||--o{ diseases : "StockCode"
    refrens ||--o{ diseases : "DiseasesRefNo"
    countref ||--o{ diseases : "C_Code"
    disref ||--o{ diseases : "DisCode"
    refrens ||--o{ disref : "DiseasesRefNo"
    species ||--o{ abnorm : "SpecCode"
    stocks ||--o{ abnorm : "StockCode"
    refrens ||--o{ abnorm : "ABNORMRefNo"
    refrens ||--o{ abnormref : "RefNo"
    refrens ||--o{ citesfb : "RefNo"
    species ||--o{ seafoodad : "Speccode"
    countref ||--o{ seafoodad : "c_code_caught"
    countref ||--o{ seafoodadref : "c_code_web"
    species ||--o{ oceanadaptspecieslinks : "speccode"
```

---

### D9 — References, Multimedia and Administration

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    occurrence {
        int OccurrenceRefNo PK
        int SpecCode FK
    }
    biblio {
        int autoctr PK
        int RefNo FK
        int SpecCode FK
    }
    biblio2 {
        int autoctr PK
        int RefNo FK
    }
    collaborators {
        string C_Code FK
    }
    institution {
        int ID PK
    }
    instlanguage {
        int ID FK
    }
    instmembership {
        int ID FK
        string C_Code FK
    }
    instspecies {
        int ID FK
        int SpecCode FK
    }
    dispic {
        int PicNum PK
        int SpecCode FK
        int StockCode FK
        int RefNo FK
    }
    fieldguide_pic {
        int id PK
        int SpecCode FK
    }
    sounds {
        int autoctr PK
        int SpecCode FK
        int Stockcode FK
        int SoundRefNo FK
    }
    withphotos {
        int SpecCode FK
    }
    withoutpicture {
        int SpecCode FK
    }
    specieswithpicture {
        int SpecCode FK
    }
    specieswithoutphoto {
        int SpecCode FK
    }
    wpicture {
        int SpecCode FK
    }
    rmcaphotos {
        int autoctr PK
        int speccode FK
        string c_code FK
    }
    museum {
        int OccurrenceRefNo FK
        string C_code FK
    }
    collectionsref {
        int OccurrenceRefNo FK
        string C_code FK
    }
    orderage {
        int AutoCtr PK
        string Order FK
    }
    acknowledge {
        int SpecCode FK
    }
    sponsors {
        int SpecCode FK
    }
    coffversions {
        int RefNo FK
    }

    refrens ||--o{ biblio : "RefNo"
    species ||--o{ biblio : "SpecCode"
    refrens ||--o{ biblio2 : "RefNo"
    countref ||--o{ collaborators : "C_Code"
    institution ||--o{ instlanguage : "ID"
    institution ||--o{ instmembership : "ID"
    countref ||--o{ instmembership : "C_Code"
    institution ||--o{ instspecies : "ID"
    species ||--o{ instspecies : "SpecCode"
    species ||--o{ dispic : "SpecCode"
    stocks ||--o{ dispic : "StockCode"
    refrens ||--o{ dispic : "RefNo"
    species ||--o{ fieldguide_pic : "SpecCode"
    species ||--o{ sounds : "SpecCode"
    stocks ||--o{ sounds : "Stockcode"
    refrens ||--o{ sounds : "SoundRefNo"
    species ||--o{ withphotos : "SpecCode"
    species ||--o{ withoutpicture : "SpecCode"
    species ||--o{ specieswithpicture : "SpecCode"
    species ||--o{ specieswithoutphoto : "SpecCode"
    species ||--o{ wpicture : "SpecCode"
    species ||--o{ rmcaphotos : "speccode"
    countref ||--o{ rmcaphotos : "c_code"
    occurrence ||--o{ museum : "OccurrenceRefNo"
    countref ||--o{ museum : "C_code"
    occurrence ||--o{ collectionsref : "OccurrenceRefNo"
    countref ||--o{ collectionsref : "C_code"
    species ||--o{ occurrence : "SpecCode"
    refrens ||--o{ coffversions : "RefNo"
    species ||--o{ acknowledge : "SpecCode"
    species ||--o{ sponsors : "SpecCode"
```

---

### D10 — Food Loss, Web Portal and Support Tables

```mermaid
erDiagram
    species {
        int SpecCode PK
    }
    stocks {
        int StockCode PK
    }
    refrens {
        int RefNo PK
    }
    countref {
        string C_Code PK
    }
    faoarref {
        int AreaCode PK
    }
    families {
        int FamCode PK
    }
    orders {
        int Ordnum PK
        string Order
    }
    fl_fish {
        int FishCode PK
        int Speccode FK
        int Stockcode FK
    }
    fl_location {
        int LocationCode PK
    }
    fl_losses {
        int LossCode PK
        int FishCode FK
        int Speccode FK
        int Stockcode FK
        int LocationCode FK
    }
    zweb_cn3 {
        int SpecCode FK
    }
    zweb_continent {
        int AreaCode FK
    }
    zweb_factsheetmaint {
        int autoctr PK
        int SpecCode FK
    }
    zweb_factsheetmaint_aquaculture {
        int autoctr PK
        int SpecCode FK
    }
    zweb_foridentification {
        int FamCode FK
        int Ordnum FK
        string C_Code FK
        int AreaCode FK
    }
    zweb_rdecomnamescountry {
        string C_Code FK
    }
    zweb_rdecountrycoordinators {
        string C_Code FK
    }
    keys {
        int RefNo FK
        int OrdNum FK
        int FamCode FK
        string C_code FK
        int AreaCode FK
    }
    keyquestions {
        int autoctr PK
        int OrdNum FK
        int FamCode FK
        int SpecCode FK
    }

    species ||--o{ fl_fish : "Speccode"
    stocks ||--o{ fl_fish : "Stockcode"
    fl_fish ||--o{ fl_losses : "FishCode"
    species ||--o{ fl_losses : "Speccode"
    stocks ||--o{ fl_losses : "Stockcode"
    fl_location ||--o{ fl_losses : "LocationCode"
    species ||--o{ zweb_cn3 : "SpecCode"
    faoarref ||--o{ zweb_continent : "AreaCode"
    species ||--o{ zweb_factsheetmaint : "SpecCode"
    species ||--o{ zweb_factsheetmaint_aquaculture : "SpecCode"
    families ||--o{ zweb_foridentification : "FamCode"
    orders ||--o{ zweb_foridentification : "Ordnum"
    countref ||--o{ zweb_foridentification : "C_Code"
    faoarref ||--o{ zweb_foridentification : "AreaCode"
    countref ||--o{ zweb_rdecomnamescountry : "C_Code"
    countref ||--o{ zweb_rdecountrycoordinators : "C_Code"
    refrens ||--o{ keys : "RefNo"
    orders ||--o{ keys : "OrdNum"
    families ||--o{ keys : "FamCode"
    countref ||--o{ keys : "C_code"
    faoarref ||--o{ keys : "AreaCode"
    orders ||--o{ keyquestions : "OrdNum"
    families ||--o{ keyquestions : "FamCode"
    species ||--o{ keyquestions : "SpecCode"
```
