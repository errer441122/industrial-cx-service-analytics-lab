# Power BI-Style Star Schema

## Fact Table

`FactCustomerFeedback`

| Column | Type | Purpose |
| --- | --- | --- |
| FeedbackId | Text | Stable feedback record key |
| DateKey | Date | Link to `DimDate` |
| SegmentKey | Text | Link to `DimCustomerSegment` |
| JourneyStageKey | Text | Link to `DimJourneyStage` |
| ChannelKey | Text | Link to `DimChannel` |
| RegionKey | Text | Link to `DimRegion` |
| SatisfactionScore | Whole number | 1-5 satisfaction score |
| FeedbackVolume | Whole number | Weighted feedback volume |
| FrictionScore | Whole number | 1-5 journey friction score |
| FollowUpRequired | Text | yes/no |
| FollowUpCompleted | Text | yes/no |
| PostActionScore | Whole number | Score after completed intervention |

## Dimensions

`DimCustomerSegment`

| Column | Purpose |
| --- | --- |
| SegmentKey | Relationship key |
| Segment | Customer profile label |
| ProfileNote | Qualitative segment context |

`DimJourneyStage`

| Column | Purpose |
| --- | --- |
| JourneyStageKey | Relationship key |
| JourneyStage | Purchase, service, ownership, or digital stage |
| StageOwner | Dealer, CX, digital, service, or CRM owner |

`DimDate`

| Column | Purpose |
| --- | --- |
| DateKey | Calendar key |
| Month | Trend grouping |
| Quarter | Quarterly reporting |

`DimChannel` and `DimRegion` support channel mix and regional follow-up reporting.

## Relationships

- `FactCustomerFeedback[DateKey]` many-to-one `DimDate[DateKey]`
- `FactCustomerFeedback[SegmentKey]` many-to-one `DimCustomerSegment[SegmentKey]`
- `FactCustomerFeedback[JourneyStageKey]` many-to-one `DimJourneyStage[JourneyStageKey]`
- `FactCustomerFeedback[ChannelKey]` many-to-one `DimChannel[ChannelKey]`
- `FactCustomerFeedback[RegionKey]` many-to-one `DimRegion[RegionKey]`

## Default Report Pages

- Customer Satisfaction Overview.
- Segment Risk and Profiling.
- Journey Friction Trend.
- Follow-up Action Tracker.
- Post-Action Improvement Review.
