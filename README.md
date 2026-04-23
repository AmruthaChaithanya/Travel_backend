## Summary
A production-grade backend for a travel booking platform built with Django and Django REST Framework.
This service provides secure user authentication, multi-modal booking, reservation management, and clean API-first architecture designed for reliability and scale.

## Problem Statement
Modern travel platforms must coordinate flight, bus, and train bookings while maintaining user trust and operational flexibility.
This backend solves fragmented booking flows by unifying reservation management, ensuring data consistency, and enabling rapid integration with frontend and third-party systems.

## Methodology
- Designed using API-first principles with DRF.
- Modeled booking workflows for flights, buses, and trains as reusable services.
- Focused on secure session handling, transaction consistency, and scalable database design.
- Delivered with a deployment pipeline targeting Railway for cloud-based production hosting.

## Features
- Secure user authentication and profile management
- Booking engine for flights, buses, and trains
- Reservation creation, modification, and cancellation
- API-driven architecture for mobile and web clients
- Role-aware access control and user session validation
- Modular services for clean separation of booking responsibilities

## Booking Workflow
  User->>Frontend: Select travel option
  
  Frontend->>Backend: POST /api/bookings/{type}
  
  Backend->>Database: Validate availability, create booking
  
  Database-->>Backend: Booking record created
  
  Backend-->>Frontend: 201 Created with reservation details
  
  Frontend-->>User: Display confirmation
    
## Tech Stack
- Backend: Django
- API: Django REST Framework
- Database: PostgreSQL
- Deployment: Railway
- Authentication: Token/session-based auth
- Dev tooling: Git, pip, virtualenv

## Results
- Delivered a modular booking backend suitable for enterprise travel systems
- Improved maintainability with clear separation between booking services and API layer
- Built to support horizontal scaling through stateless request handling and centralized persistence
- Positioned for integration with web and mobile frontends via a consistent REST contract
