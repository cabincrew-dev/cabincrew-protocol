# CabinCrew Protocol Node.js Library

This library provides TypeScript interfaces for the CabinCrew Protocol schemas.

## Installation

```bash
npm install @cabincrew/protocol
```

## Usage

```typescript
import { Artifact } from '@cabincrew/protocol';

const artifact: Artifact = {
  artifact_type: 'file',
  action: 'create',
  mime: 'text/plain',
  body: 'Hello world'
};
```
