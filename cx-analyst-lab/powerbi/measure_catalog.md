# Power BI-Style Measure Catalog

## Core Measures

```DAX
Weighted Feedback Volume =
SUM ( FactCustomerFeedback[FeedbackVolume] )
```

```DAX
Customer Satisfaction Rate =
DIVIDE (
    CALCULATE (
        [Weighted Feedback Volume],
        FactCustomerFeedback[SatisfactionScore] >= 4
    ),
    [Weighted Feedback Volume]
)
```

```DAX
At-Risk Segment Count =
COUNTROWS (
    FILTER (
        VALUES ( DimCustomerSegment[Segment] ),
        [Weighted Avg Satisfaction] < 3.5
            || [Journey Friction Index] >= 3.5
    )
)
```

```DAX
Journey Friction Index =
DIVIDE (
    SUMX (
        FactCustomerFeedback,
        FactCustomerFeedback[FrictionScore] * FactCustomerFeedback[FeedbackVolume]
    ),
    [Weighted Feedback Volume]
)
```

```DAX
Follow-up Completion Rate =
DIVIDE (
    CALCULATE (
        COUNTROWS ( FactCustomerFeedback ),
        FactCustomerFeedback[FollowUpCompleted] = "yes"
    ),
    CALCULATE (
        COUNTROWS ( FactCustomerFeedback ),
        FactCustomerFeedback[FollowUpRequired] = "yes"
    )
)
```

```DAX
Post-Action Improvement Delta =
AVERAGEX (
    FILTER (
        FactCustomerFeedback,
        FactCustomerFeedback[FollowUpCompleted] = "yes"
    ),
    FactCustomerFeedback[PostActionScore] - FactCustomerFeedback[SatisfactionScore]
)
```

## Supporting Measures

```DAX
Weighted Avg Satisfaction =
DIVIDE (
    SUMX (
        FactCustomerFeedback,
        FactCustomerFeedback[SatisfactionScore] * FactCustomerFeedback[FeedbackVolume]
    ),
    [Weighted Feedback Volume]
)
```

```DAX
Open Follow-up Count =
CALCULATE (
    COUNTROWS ( FactCustomerFeedback ),
    FactCustomerFeedback[FollowUpRequired] = "yes",
    FactCustomerFeedback[FollowUpCompleted] = "no"
)
```
