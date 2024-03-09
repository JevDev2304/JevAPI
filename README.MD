# FastAPI v0.1.0 🚀

## Overview
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. 🐍✨

## OpenAPI Specification (OAS) Version
This API adheres to the OpenAPI Specification version 3.1. 📜

## Endpoints

### Owner 👤

- **GET /owner/**
  - Retrieve a list of all owners.

- **PUT /owner/**
  - Update owner information.

- **POST /owner/**
  - Create a new owner.

- **GET /owner/{id}**
  - Retrieve information about a specific owner by ID.

- **DELETE /owner/{id}**
  - Delete an owner by ID.

- **GET /owner/{field}/{key}**
  - Search owners by a specific attribute.

### House 🏠

- **GET /house/**
  - Retrieve a list of all houses.

- **PUT /house/**
  - Update house information.

- **POST /house/**
  - Create a new house.

- **GET /house/{id}**
  - Retrieve information about a specific house by ID.

- **DELETE /house/{id}**
  - Delete a house by ID.

- **GET /house/{field}/{key}**
  - Search houses by a specific attribute.

### Report 📊

- **GET /report/**
  - Retrieve a list of all reports.

- **PUT /report/**
  - Update report information.

- **POST /report/**
  - Create a new report.

- **GET /report/{id}**
  - Retrieve information about a specific report by ID.

- **DELETE /report/{id}**
  - Delete a report by ID.

- **GET /report/{field}/{key}**
  - Search reports by a specific attribute.

### Worker 👷

- **GET /worker/**
  - Retrieve a list of all workers.

- **PUT /worker/**
  - Update worker information.

- **POST /worker/**
  - Create a new worker.

- **GET /worker/{id}**
  - Retrieve information about a specific worker by ID.

- **DELETE /worker/{id}**
  - Delete a worker by ID.

- **GET /worker/{field}/{key}**
  - Search workers by a specific attribute.

### Lease 📅

- **GET /lease/**
  - Retrieve a list of all leases.

- **PUT /lease/**
  - Update lease information.

- **POST /lease/**
  - Create a new lease.

- **GET /lease/{id}**
  - Retrieve information about a specific lease by ID.

- **DELETE /lease/{id}**
  - Delete a lease by ID.

- **GET /lease/{field}/{key}**
  - Search leases by a specific attribute.

## Search by Attribute 🔍
For each resource type (owner, house, report, worker, lease), you can perform a search using the `{field}/{key}` endpoint.

Feel free to explore and use FastAPI for your API development needs! 🚀✨
