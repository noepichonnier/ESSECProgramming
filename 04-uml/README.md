# Exercise 4 – UML practice (slide 68)

All diagrams are written in [Mermaid](https://mermaid.js.org/), which GitHub renders directly
in this file. Mermaid has no native *use case* diagram, so those are drawn as flowcharts
(actors = rounded boxes, use cases = ovals, system boundary = subgraph).

- [Exo 1 – Hospital Management System](#exo-1--hospital-management-system)
- [Exo 2 – ABCD Records](#exo-2--abcd-records)

---

# Exo 1 – Hospital Management System

## Task 1 – Basic class diagram (Patient, Doctor, Organizer)

```mermaid
classDiagram
    class Patient {
        -int id
        -String name
        -String password
        -String email
        +login() bool
        +submitProblem(description) void
        +pay(amount, method) void
    }
    class Doctor {
        -int id
        -String name
        -String password
        -String speciality
        +login() bool
        +writePrescription(problem) void
        +receivePayment(amount) void
    }
    class Organizer {
        -int id
        -String name
        -String password
        -String email
        +readProblem() void
        +forwardToDoctor(doctor) void
        +sendPrescription(patient) void
        +forwardPayment(doctor) void
    }
    Organizer "1" --> "0..*" Patient : manages / sends prescriptions to
    Organizer "1" --> "1..*" Doctor : consults / pays
    Patient "0..*" -- "0..*" Doctor : is treated by
```

Who interacts with whom: the **Organizer** is the hub between patients and doctors – the
patient never talks to the doctor directly (steps 2, 4 and 6 of the specification).

## Task 2 – Complete class diagram (6 classes + payment types)

```mermaid
classDiagram
    class Patient {
        -int id
        -String name
        -String password
        +submitProblem(description) HealthProblem
        +pay(prescription, method) Payment
    }
    class Doctor {
        -int id
        -String name
        -String speciality
        +writePrescription(problem) Prescription
    }
    class Organizer {
        -int id
        -String name
        +readProblem(problem) void
        +consultDoctor(problem, doctor) void
        +sendPrescription(prescription) void
        +forwardPayment(payment) void
    }
    class HealthProblem {
        -int id
        -String description
        -Date submittedAt
    }
    class Prescription {
        -int id
        -String solution
        -double fee
        -Date issuedAt
    }
    class Payment {
        <<abstract>>
        -int id
        -double amount
        -Date paidAt
        +process() bool
    }
    class Check {
        -String checkNumber
        +process() bool
    }
    class Cash {
        +process() bool
    }
    class CreditCard {
        -String cardNumber
        -String holder
        +process() bool
    }

    Patient "1" --> "0..*" HealthProblem : submits
    HealthProblem "1" --> "0..1" Prescription : leads to
    Doctor "1" --> "0..*" Prescription : writes
    Organizer "1" --> "0..*" HealthProblem : reads
    Prescription "1" --> "0..1" Payment : settled by
    Payment <|-- Check
    Payment <|-- Cash
    Payment <|-- CreditCard
```

**Sequence diagram – one patient submits a problem, receives a prescription and pays**

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as Platform
    actor O as Organizer
    actor D as Doctor
    P->>S: submitProblem(description)
    S-->>O: new HealthProblem
    O->>D: consult(problem)
    D-->>O: Prescription
    O->>P: sendPrescription()
    P->>S: pay(amount, method)
    S-->>O: Payment received
    O->>D: forwardPayment()
```

## Task 3 – Advanced model

Additions: `User` superclass, polymorphic payment (Strategy), `HealthProblem` status tracking,
timestamps, and a link to past prescriptions.

```mermaid
classDiagram
    class User {
        <<abstract>>
        -int id
        -String name
        -String password
        +login() bool
        +logout() void
    }
    class Patient {
        -String email
        +submitProblem(description) HealthProblem
        +pay(prescription, strategy) Payment
        +history() List~Prescription~
    }
    class Doctor {
        -String speciality
        +writePrescription(problem) Prescription
    }
    class Organizer {
        +readProblem(problem) void
        +consultDoctor(problem, doctor) void
        +sendPrescription(prescription) void
        +forwardPayment(payment) void
        +createMember(role) User
        +updateSystem() void
    }
    class HealthProblem {
        -int id
        -String description
        -Status status
        -DateTime createdAt
        -DateTime updatedAt
    }
    class Status {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class Prescription {
        -int id
        -String solution
        -double fee
        -DateTime issuedAt
        -Prescription previous
    }
    class Payment {
        -int id
        -double amount
        -DateTime paidAt
        -PaymentStrategy strategy
        +execute() bool
    }
    class PaymentStrategy {
        <<interface>>
        +pay(amount) bool
    }
    class CheckPayment {
        -String checkNumber
        +pay(amount) bool
    }
    class CashPayment {
        +pay(amount) bool
    }
    class CreditCardPayment {
        -String cardNumber
        +pay(amount) bool
    }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" --> "0..*" HealthProblem : submits
    HealthProblem --> Status
    HealthProblem "1" --> "0..*" Prescription : resolved by
    Doctor "1" --> "0..*" Prescription : writes
    Prescription "0..1" --> "0..1" Prescription : previous
    Prescription "1" --> "0..*" Payment : paid by
    Payment o-- PaymentStrategy
    PaymentStrategy <|.. CheckPayment
    PaymentStrategy <|.. CashPayment
    PaymentStrategy <|.. CreditCardPayment
    Organizer "1" --> "0..*" Patient : registers
```

### Sequence 1 – Patient registration

```mermaid
sequenceDiagram
    actor O as Organizer
    participant S as System
    participant DB as Database
    O->>S: createMember(name, email, role)
    S->>S: generate id + password
    S->>DB: save(new Patient)
    DB-->>S: ok
    S-->>O: member id + password
    O-->>O: communicate credentials to the patient
```

### Sequence 2 – Consultation flow

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as System
    actor O as Organizer
    actor D as Doctor
    P->>S: submitProblem(description)
    S->>S: create HealthProblem (PENDING)
    S-->>O: notify new problem
    O->>S: readProblem(id)
    S->>S: status = IN_REVIEW
    O->>D: consultDoctor(problem)
    D->>S: writePrescription(problem, solution, fee)
    S->>S: status = RESOLVED
    S-->>O: prescription ready
    O->>P: sendPrescription()
```

### Sequence 3 – Payment processing

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as System
    participant PS as PaymentStrategy
    actor O as Organizer
    actor D as Doctor
    P->>S: pay(prescription, strategy)
    S->>PS: pay(amount)
    alt payment accepted
        PS-->>S: true
        S->>S: store Payment (paidAt = now)
        S-->>O: payment received
        O->>D: forwardPayment(amount)
        D-->>O: acknowledgement
        S-->>P: receipt
    else payment refused
        PS-->>S: false
        S-->>P: error, try another method
    end
```

### Questions to consider

1. **A patient consulting several doctors?** Make the problem–doctor link many-to-many through
   `Prescription`: one `HealthProblem` can have several `Prescription`s, each written by a different
   doctor (`Doctor 1 → 0..* Prescription`, `HealthProblem 1 → 0..* Prescription`).
2. **Reusable prescriptions?** Separate the *template* (treatment/solution text) from the *issued
   prescription* (patient, date, fee). The `previous` reference lets a renewal point to the original.
3. **Which design pattern for payments?** **Strategy**: `PaymentStrategy` with `Check`, `Cash`,
   `CreditCard` implementations that can be swapped at runtime (a Factory can build the right one).
4. **Data integrity for payments?** Run payment + status update + forwarding in a single database
   transaction (atomic, all-or-nothing); make the payment request idempotent (unique payment id
   so a retry does not charge twice); validate amount = prescription fee; keep an audit log.

---

# Exo 2 – ABCD Records

## Level 1

### Task 1.1 – Use case diagram

```mermaid
flowchart LR
    M(["Member"])
    C(["Order Processing Clerk"])
    subgraph SYS["ABCD Records system"]
        UC1(["Place Order"])
        UC2(["Verify Membership"])
        UC3(["Process Order"])
        UC4(["Make Payment"])
    end
    M --- UC1
    M --- UC4
    C --- UC2
    C --- UC3
    UC1 -.->|"«include»"| UC2
```

### Task 1.2 – Class diagram

```mermaid
classDiagram
    class Member {
        -int memberId
        -String name
        -String address
        -String memberClass
        +placeOrder() Order
        +makePayment(order) void
    }
    class Order {
        -int orderId
        -Date date
        -String status
        -double total
        +calculateTotal() double
    }
    class OrderProcessingClerk {
        -int clerkId
        -String name
        +verifyMembership(member) bool
        +processOrder(order) void
    }
    Member "1" --> "0..*" Order : places
    OrderProcessingClerk "1" --> "0..*" Order : processes
    OrderProcessingClerk ..> Member : verifies
```

## Level 2

### Task 2.1 – Complete use case diagram

```mermaid
flowchart LR
    NM(["Non-Member"])
    M(["Member"])
    OC(["Order Processing Clerk"])
    CC(["Collection Department Clerk"])
    subgraph SYS["ABCD Records system"]
        SMA(["Send Membership Application"])
        PO(["Place Order"])
        VM(["Verify Membership"])
        VIA(["Verify Item Availability"])
        AD(["Apply Discount"])
        OUI(["Order Unavailable Items"])
        PROC(["Process Order"])
        PI(["Print Invoice"])
        PSL(["Print Shipping List"])
        MP(["Make Payment"])
        CP(["Collect Payment"])
    end
    NM --- SMA
    M --- PO
    M --- MP
    OC --- PROC
    OC --- VM
    CC --- CP

    PO -.->|"«include»"| VM
    PO -.->|"«include»"| VIA
    PROC -.->|"«include»"| PI
    PROC -.->|"«include»"| PSL
    MP -.->|"«include»"| CP
    AD -.->|"«extend» (Royal member)"| PO
    OUI -.->|"«extend» (item unavailable, Royal member)"| PO
    SMA -.->|"«extend» (not a member)"| VM
```

### Task 2.2 – Complete class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        -int memberId
        -String name
        -String address
        +placeOrder() Order
        +discountRate() double
        +canOrderUnavailable() bool
    }
    class RoyalMember {
        +discountRate() double
        +canOrderUnavailable() bool
    }
    class RegularMember {
        +discountRate() double
        +canOrderUnavailable() bool
    }
    class Order {
        -int orderId
        -Date date
        -String status
        +addLine(item, qty) void
        +total() double
    }
    class OrderLine {
        -int quantity
        -double unitPrice
        -bool backordered
        +subtotal() double
    }
    class Item {
        <<abstract>>
        -int itemId
        -String title
        -double price
        -int stock
        +isAvailable() bool
    }
    class CD
    class Tape
    class Invoice {
        -int invoiceNo
        -Date date
        -double amount
        +print() void
    }
    class ShippingList {
        -int listNo
        -Date date
        +print() void
    }
    class Payment {
        <<abstract>>
        -double amount
        -Date date
        +process() bool
    }
    class Cash
    class Check {
        -String checkNumber
    }
    class BankDraft {
        -String draftNumber
    }
    class MembershipApplication {
        -String applicantName
        -String address
        -Date date
        -String status
    }
    class OrderProcessingClerk {
        +verifyMembership(m) bool
        +processOrder(o) void
    }
    class CollectionDepartmentClerk {
        +collectPayment(p) void
    }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" --> "0..1" Invoice : generates
    Order "1" --> "0..1" ShippingList : generates
    Order "1" --> "0..*" Payment : paid by
    OrderProcessingClerk "1" --> "0..*" Order : processes
    CollectionDepartmentClerk "1" --> "0..*" Payment : collects
    MembershipApplication "0..*" --> "0..1" Member : becomes
```

**Scenario – a Royal member orders 2 CDs (one unavailable) and pays by check**

```mermaid
classDiagram
    class m1 ["m1 : RoyalMember"]
    class o1 ["o1 : Order"]
    class l1 ["l1 : OrderLine (backordered = false)"]
    class l2 ["l2 : OrderLine (backordered = true)"]
    class cd1 ["cd1 : CD (stock = 5)"]
    class cd2 ["cd2 : CD (stock = 0)"]
    class inv ["inv : Invoice"]
    class pay ["pay : Check"]
    m1 --> o1
    o1 *-- l1
    o1 *-- l2
    l1 --> cd1
    l2 --> cd2
    o1 --> inv
    o1 --> pay
```

## Level 3 – Sequence diagrams

### 1. Complete order processing flow

```mermaid
sequenceDiagram
    actor M as Member
    participant S as System
    actor OC as Order Processing Clerk
    actor CC as Collection Dept. Clerk
    participant R as Daily Records File
    M->>S: placeOrder(items)
    S->>OC: verify membership
    OC-->>S: member valid
    loop for each order line
        S->>S: check item availability
    end
    S->>S: apply discount (Royal)
    OC->>S: processOrder()
    S->>S: print Invoice + Shipping List
    S-->>M: invoice
    M->>CC: payment (cash / check / bank draft)
    CC-->>S: payment recorded
    S->>R: save order
```

### 2. Membership verification (success and failure)

```mermaid
sequenceDiagram
    actor U as Customer
    participant S as System
    actor OC as Order Processing Clerk
    U->>S: placeOrder()
    S->>OC: verifyMembership(customer)
    alt customer is a member
        OC-->>S: valid (Royal / Regular)
        S-->>U: order accepted
    else not a member
        OC-->>S: invalid
        S-->>U: send MembershipApplication form
        U-->>S: returns completed form (optional)
    end
```

### 3. Payment processing (all types)

```mermaid
sequenceDiagram
    actor M as Member
    participant S as System
    actor CC as Collection Dept. Clerk
    M->>S: pay(order, type)
    alt Cash
        S->>CC: receive cash
    else Check
        S->>CC: receive check
        CC->>CC: verify check
    else Bank Draft
        S->>CC: receive bank draft
        CC->>CC: verify draft
    end
    CC-->>S: payment confirmed
    S->>S: order.status = PAID
    S-->>M: receipt
```

### 4. Item reordering for Royal members

```mermaid
sequenceDiagram
    actor M as Royal Member
    participant S as System
    participant I as Item
    participant OC as Order Processing Clerk
    M->>S: order(item)
    S->>I: isAvailable()
    I-->>S: false
    alt member is Royal
        S->>S: create backordered OrderLine
        S-->>OC: reorder request (priority)
        OC->>OC: restock item
        S-->>M: order accepted, shipped when available
    else Regular member
        S-->>M: item unavailable, order refused
    end
```
