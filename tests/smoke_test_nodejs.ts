#!/usr/bin/env node
/**
 * Smoke test for TypeScript/Node.js library.
 * Tests basic import and instantiation of generated types.
 */

import {
    EngineOutput,
    EngineInput,
    PlanToken,
    AuditEvent,
    Status,
    Mode,
    Decision,
    State,
} from '../lib/nodejs/src/protocol';

function testImports(): boolean {
    console.log('Testing imports...');
    // If we got here, imports worked
    console.log('✓ All imports successful');
    return true;
}

function testEnumValues(): boolean {
    console.log('Testing enum values...');

    // Status and Mode are type aliases, not enums
    // They are defined as: type Status = "success" | "failure"
    const successStatus: Status = 'success';
    const failureStatus: Status = 'failure';
    const flightPlanMode: Mode = 'flight-plan';
    const takeOffMode: Mode = 'take-off';

    if (successStatus !== 'success' || failureStatus !== 'failure') {
        console.log('✗ Status type values incorrect');
        return false;
    }

    if (flightPlanMode !== 'flight-plan' || takeOffMode !== 'take-off') {
        console.log('✗ Mode type values incorrect');
        return false;
    }

    console.log('✓ Type values correct');
    return true;
}

function testInstantiation(): boolean {
    console.log('Testing type instantiation...');

    const output: EngineOutput = {
        engine_id: 'test-engine',
        mode: 'flight-plan',
        protocol_version: '1.0.0',
        receipt_id: 'receipt-123',
        status: 'success',
    };

    if (output.engine_id !== 'test-engine') {
        console.log('✗ Object instantiation failed');
        return false;
    }

    console.log('✓ Type instantiation successful');
    return true;
}

function testTypeChecking(): boolean {
    console.log('Testing TypeScript type checking...');

    // This should compile without errors
    const output: EngineOutput = {
        engine_id: 'test',
        mode: 'flight-plan',
        protocol_version: '1.0.0',
        receipt_id: 'r1',
        status: 'success',
        error: 'optional error',
        warnings: ['warning1', 'warning2'],
    };

    console.log('✓ Type checking working');
    return true;
}

function testJsonSerialization(): boolean {
    console.log('Testing JSON serialization...');

    const output: EngineOutput = {
        engine_id: 'test',
        mode: 'flight-plan',
        protocol_version: '1.0.0',
        receipt_id: 'r1',
        status: 'success',
    };

    const json = JSON.stringify(output);
    const parsed = JSON.parse(json) as EngineOutput;

    if (parsed.engine_id !== output.engine_id) {
        console.log('✗ JSON serialization failed');
        return false;
    }

    console.log('✓ JSON serialization working');
    return true;
}

function main(): number {
    console.log('='.repeat(60));
    console.log('CabinCrew Protocol - TypeScript Library Smoke Tests');
    console.log('='.repeat(60));

    const tests = [
        testImports,
        testEnumValues,
        testInstantiation,
        testTypeChecking,
        testJsonSerialization,
    ];

    let passed = 0;
    let failed = 0;

    for (const test of tests) {
        try {
            if (test()) {
                passed++;
            } else {
                failed++;
            }
        } catch (e) {
            console.log(`✗ ${test.name} failed with exception:`, e);
            failed++;
        }
    }

    console.log('='.repeat(60));
    console.log(`Results: ${passed} passed, ${failed} failed`);
    console.log('='.repeat(60));

    return failed === 0 ? 0 : 1;
}

if (typeof process !== 'undefined') {
    process.exit(main());
} else {
    main();
}
