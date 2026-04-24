# FishTrack API

## Definition

FishTrack is the API for tracking and recording aquatic species observed during aquarium visits. It provides a checklist of species a user has seen at one or more aquariums, functioning as a personal taxonomic visit log.

## Purpose

FishTrack allows users to record and query which species they have observed at specific aquariums. Each record links a species to the aquarium where it was spotted, enabling the construction of a personal or institutional observation history.

## Checklist Concept

A checklist in FishTrack represents the collection of species confirmed at a given aquarium:

- Each species can be marked as "seen" at one or more aquariums
- Records include metadata such as visit date and optional notes
- The model is extensible and can later be scoped by region, habitat type, rarity level, etc.

## Current Scope

This initial version establishes the base FastAPI project structure. Endpoints and data models will be defined in future user stories as the domain model is refined.

## Port

`8005`

## Running

```bash
make run
# Server at http://localhost:8005
# Swagger UI at http://localhost:8005/docs
```
