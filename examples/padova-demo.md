# Apartment hunting with Grokbot: fictional Padova example

All listings, prices and descriptions below are fictional. No landlord details or real housing search data are included. The original search was Grokbot-assisted; this example demonstrates the portable skill.

User request: "Compare these three Padova rooms against a fictional EUR 600 all-in monthly budget. I need a private room. Keep unknown costs visible and map only supported locations."

| ID | Fictional source | Listing evidence |
| --- | --- | --- |
| demo-a | https://example.com/rooms/a | Private room in Centro. Rent EUR 470/month plus fixed EUR 80/month covering all bills. Refundable deposit EUR 940. Approximate neighborhood coordinates: 45.407, 11.877. |
| demo-b | https://example.com/rooms/b | Private room in Arcella. Rent EUR 430/month; "bills extra" with no amount. Deposit not stated. No supported location beyond the neighborhood name. |
| demo-c | https://example.com/rooms/c | Private room in Portello. Rent EUR 520/month plus EUR 110/month covering all bills. No one-time fee or deposit stated. |

Expected shortlist:

| Room | Monthly cost | Move-in cash | Status | Next question |
| --- | --- | --- | --- | --- |
| Centro | EUR 550 all-in | EUR 1,490 for first month + refundable deposit | Fits the stated room/budget requirements | Confirm availability and viewing details |
| Arcella | At least EUR 430, bills unknown | Unknown | Confirm costs/details | What is the total recurring bill amount and deposit? |
| Portello | EUR 630 all-in | At least EUR 630; deposit/fees unknown | Over budget | Does the landlord offer a lower all-in price? |

The cheapest base rent does not win automatically. Arcella remains unconfirmed until bills are known. Only Centro gets a map pin, labeled approximate neighborhood location; no precise address is implied.

Suggested public demo sequence: show these fictional inputs, run `$apartment-hunt`, compare the three resulting statuses, then open the approximate Centro pin. Caption: "Apartment hunting with Grokbot. Links in, costs and unanswered questions out."
