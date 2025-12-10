#!/usr/bin/env python3
"""
Smoke test for Python library.
Tests basic import and instantiation of generated Pydantic models.
"""
import sys
from pathlib import Path

# Add lib to path
lib_path = Path(__file__).parent.parent / "lib" / "python" / "src"
sys.path.insert(0, str(lib_path))

def test_imports():
    """Test that all major types can be imported."""
    print("Testing imports...")
    from cabincrew_protocol.protocol import (
        EngineOutput,
        EngineInput,
        PlanToken,
        AuditEvent,
        Status,
        Mode,
        Decision,
        State,
    )
    print("✓ All imports successful")
    return True

def test_enum_values():
    """Test that enums have expected values."""
    print("Testing enum values...")
    from cabincrew_protocol.protocol import Status, Mode, Decision
    
    assert hasattr(Status, 'success')
    assert hasattr(Status, 'failure')
    assert hasattr(Mode, 'flight_plan')
    assert hasattr(Mode, 'take_off')
    assert hasattr(Decision, 'allow')
    assert hasattr(Decision, 'deny')
    
    print("✓ Enum values correct")
    return True

def test_instantiation():
    """Test that models can be instantiated with required fields."""
    print("Testing model instantiation...")
    from cabincrew_protocol.protocol import EngineOutput, Status, Mode
    
    # Test with required fields
    output = EngineOutput(
        engine_id="test-engine",
        mode="flight-plan",
        protocol_version="1.0.0",
        receipt_id="receipt-123",
        status="success"
    )
    
    assert output.engine_id == "test-engine"
    assert output.status == Status.success
    assert output.mode == Mode.flight_plan
    
    print("✓ Model instantiation successful")
    return True

def test_validation():
    """Test that Pydantic validation works."""
    print("Testing validation...")
    from cabincrew_protocol.protocol import EngineOutput
    from pydantic import ValidationError
    
    # Test missing required field
    try:
        EngineOutput(
            engine_id="test",
            mode="flight-plan",
            protocol_version="1.0.0"
            # Missing receipt_id and status
        )
        print("✗ Validation should have failed for missing required fields")
        return False
    except ValidationError as e:
        print(f"✓ Validation correctly rejected missing fields: {len(e.errors())} errors")
        return True

def test_json_serialization():
    """Test JSON serialization/deserialization."""
    print("Testing JSON serialization...")
    from cabincrew_protocol.protocol import EngineOutput
    
    output = EngineOutput(
        engine_id="test",
        mode="flight-plan",
        protocol_version="1.0.0",
        receipt_id="r1",
        status="success"
    )
    
    # Serialize to JSON
    json_str = output.model_dump_json()
    assert "test" in json_str
    assert "success" in json_str
    
    # Deserialize from JSON
    output2 = EngineOutput.model_validate_json(json_str)
    assert output2.engine_id == output.engine_id
    
    print("✓ JSON serialization working")
    return True

def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("CabinCrew Protocol - Python Library Smoke Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_enum_values,
        test_instantiation,
        test_validation,
        test_json_serialization,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
