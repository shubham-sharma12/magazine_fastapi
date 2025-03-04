# Requirements for Magazine Subscription Service

You are being asked to develop a backend using FastAPI for a (simplified) magazine subscription service. This backend service would expose a REST API that enables users to:

1. Register, login, and reset their passwords.
2. Retrieve a list of magazines available for subscription. This list should include the plans available for each magazine and the discount offered for each plan.
3. Create a subscription for a magazine.
4. Retrieve, modify, and delete their subscriptions.

## Data Models Overview

### Magazine

A `magazine` that is available for subscription. Includes metadata about the magazine such as the `name`, `description`, and a `base_price` (which is the price charged for a monthly subscription). The `base_price` is a numerical value and must be greater than zero.

### Plan

Plans to which users can subscribe their magazines. There are 4 plans available in the system as described below.

A `Plan` object has the following properties: `title`, a `description`, a `renewalPeriod`, `discount` - a percentage, expressed as a decimal - for this plan (e.g. a `discount` of `0.1` means a 10% discount),and a `tier`. The `tier` is a numerical value that represents the level of the plan. The higher the `tier`, the more expensive the plan.

The `renewalPeriod` is a numerical value that represents the number of months in which the subscription would renew. Renewal periods CANNOT be zero. For example, a `renewalPeriod` of `3` means that the subscription renews every 3 months.

The 4 plans that you must support are given below.

#### Silver Plan

- title: "Silver Plan"
- description: "Basic plan which renews monthly"
- renewalPeriod: 1
- tier: 1
- discount: 0.0

#### Gold Plan

- title: "Gold Plan"
- description: "Standard plan which renews every 3 months"
- renewalPeriod: 3
- tier: 2
- discount: 0.05

#### Platinum Plan

- title: "Platinum Plan"
- description: "Premium plan which renews every 6 months"
- renewalPeriod: 6
- tier: 3
- discount: 0.10

#### Diamond Plan

- title: "Diamond Plan"
- description: "Exclusive plan which renews annually"
- renewalPeriod: 12
- tier: 4
- discount: 0.25

### Subscription

A `Subscription` tracks which `Plan` is associated with which `Magazine` for a specific `User`. The subscription also tracks the price at renewal for that magazine and the next renewal date.

A `User` can have only one `Subscription` for a specific `Magazine` and `Plan` at a time. The `Subscription` object has the following properties: `user_id`, `magazine_id`, `plan_id`, `price`, `renewal_date`, and `is_active`.

The price at renewal is calculated as the `base_price` of the magazine discounted by the `discount` of the plan. For example, if the base price of the magazine is `100` and the plan discount is `0.10`, the price will be `90`. The `price` is a numerical value and must be greater than zero.

For record keeping purposes, subscriptions are never deleted. If a user cancels a subscription to a magazine, the corresponding `is_active` attribute of that `Subscription` is set to `False`. Inactive subscriptions are never returned in the response when the user queries their subscriptions.


## Business Rules

1. Subscriptions can be modified before the expiry of the subscription period. For example, if a user has subscribed to a magazine with a `Silver Plan` and decides to upgrade to a `Gold Plan`, the `Silver Plan` subscription is deactivated and a new subscription is created with a new renewal date for the `Gold Plan` that the user has chosen.
2. If a user modifies their subscription for a magazine, the corresponding subsciption is deactivated and a new subscription is created with a new renewal date depending on the plan that is chosen by the user.
    1. For this purpose assume that there is no proration of the funds and no refunds are issued.