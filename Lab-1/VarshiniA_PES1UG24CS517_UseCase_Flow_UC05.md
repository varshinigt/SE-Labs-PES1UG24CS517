# Use-Case Flow Specification

**Name:** Varshini A  
**SRN:** PES1UG24CS517  
**Section:** I  
**Course:** Software Engineering (UE24CS341A)  
**Problem Statement:** #28 - Inter-City Freight Load Matching Marketplace  
**Use Case:** UC-05 - Release Milestone Payment

## Goal
Release the escrowed milestone payment to the awarded Freight Carrier after the submitted electronic proof of delivery (e-POD) is verified, while recording the final shipment status and notifying the affected parties.

## Actors
- **Freight Carrier (primary):** receives the milestone payment after valid delivery proof is verified.
- **Payment Gateway (supporting external system):** authenticates the payment-release request and processes the transfer.
- **Shipper (secondary):** receives payment-release confirmation.

## Preconditions
- The freight load has been posted and awarded.
- Delivery is complete.
- The milestone payment is held in escrow for the awarded shipment.

## Trigger
The system receives the e-POD submitted by the awarded carrier through UC-04 (Submit Proof of Delivery).

## Postconditions
- **Success:** payment is transferred, status becomes `Delivered - Payment Released`, and the shipper and carrier are notified.
- **Failure:** no payment is released and the funds remain in escrow.

## Main Success Scenario
1. The system receives the e-POD submitted by the awarded carrier in UC-04.
2. The system invokes UC-06 (Verify Proof of Delivery) to validate the digital signature, GPS geo-tag, and timestamp. [`«include» UC-06`]
3. UC-06 returns a successful verification result.
4. The system sends a payment-release instruction for the escrowed milestone amount to the Payment Gateway.
5. The Payment Gateway authenticates the request and processes the transfer to the carrier over an encrypted channel.
6. The system receives confirmation that the transfer completed within 60 seconds of the verified e-POD submission (NFR-001).
7. The system updates the shipment status to `Delivered - Payment Released`.
8. The system sends payment-release confirmation to both the shipper and the carrier.
9. The use case ends successfully.

## Alternate Flow - 3a. e-POD Verification Failure
- **3a1.** UC-06 returns a failed verification result because one or more required e-POD components cannot be validated.
- **3a2.** The system keeps the payment in escrow and does not send a payment-release instruction to the Payment Gateway.
- **3a3.** The system notifies the carrier that verification failed and prompts resubmission through UC-08; UC-05 ends without releasing payment.

## Special Requirement
NFR-001 requires milestone payment disbursement within 60 seconds of verified e-POD submission and encrypted communication with the Payment Gateway.
