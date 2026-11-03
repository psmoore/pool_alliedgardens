# Allied Gardens Pool (City of San Diego) — unofficial preview

A mock-up of the [City of San Diego's Allied Gardens Pool page](https://www.sandiego.gov/park-and-recreation/centers/aquatics/alliedgardens)
(pool page, Aquatic Programs, Admission Fees) with the pool on one live [Pool Relay](https://www.poolrelay.com) schedule.
Not operated by or affiliated with the City of San Diego.

No schedule is typed into the pages. Lap swim, rec swim, classes, Youth Aquatic League teams and closures are filled by
`finder.js` from the live Pool Relay view; `build.py` holds only fees, ages, rules and facts about the water.

- `build.py`: generates the three pages.
- `finder.js`: `#today`, `#week`, and `data-live` elements (`hours`, `when`, `exceptions`, `closures`; `data-ahead` widens the closure window).
- Pool Relay view: `wukjy7eHCAdsiElT58FrHm` (Allied Gardens Pool, lane by lane).
