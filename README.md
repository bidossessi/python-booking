# Booking Service

![main](https://github.com/bidossessi/python-booking/actions/workflows/tests.yml/badge.svg?branch=main)


This project is an attempt to provide a product-agnostic booking sub-system.

## Booking is a generic concept

The idea is that whether it's hotel rooms or DVDs or plane tickets or maybe a body-guard, the concept of booking remains the same. There's always:

- a `resource` that can be booked / rented / leased for a certain amount of time 
- the act of allocating that resource for a specific timeframe is generally called a `booking`,
- and a booking can be `recurrent` according to certain rules.

The projected process is that a client system would
1. register `Resource`s using their own `reference_id` (hopefully unique in the client system), and potentially a list of `tags`, and receive a `resource_id` in return they can use to create a mapping.
2. create `Booking`s by providing  the `resource_id`, a client-generated `order_id`, `date_start` and `date_end` dates, with an optional `recurrence` rule, and receive in return a `booking_id` as confirmation. This `booking_id` could be attached to an internal object representing the booking, with additionnal business-specific metadata, etc.
3. have a JSON list of bookings available through an HTTP endpoint, and (future) an iCal URL.
4. query resource availability through the `/free` endpoint, essentially outsourcing that logic.

## Current state

Currently, the `HTTP` transport is implemented with [FastAPI](https://fastapi.tiangolo.com/).

Recurrence is not yet implemented. Most probably, it  will be done with [rrule](https://dateutil.readthedocs.io/en/stable/rrule.html). 

There's only an in-memory repository to start fleshing out the concepts. However, since the value of the system
is in being able to query lots of data, an SQL repository will be the next target.