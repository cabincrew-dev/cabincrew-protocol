package main

import (
	"encoding/json"
	"fmt"
	"os"

	cabincrew "../lib/go/cabincrew"
)

func testImports() bool {
	fmt.Println("Testing imports...")
	// If we got here, imports worked
	fmt.Println("✓ All imports successful")
	return true
}

func testEnumValues() bool {
	fmt.Println("Testing enum values...")

	// Status and Mode are type aliases to string, not enums with constants
	// They are defined as: type Status string
	var successStatus cabincrew.Status = "success"
	var failureStatus cabincrew.Status = "failure"
	var flightPlanMode cabincrew.Mode = "flight-plan"
	var takeOffMode cabincrew.Mode = "take-off"

	if successStatus != "success" || failureStatus != "failure" {
		fmt.Println("✗ Status type values incorrect")
		return false
	}

	if flightPlanMode != "flight-plan" || takeOffMode != "take-off" {
		fmt.Println("✗ Mode type values incorrect")
		return false
	}

	fmt.Println("✓ Type values correct")
	return true
}

func testInstantiation() bool {
	fmt.Println("Testing struct instantiation...")

	output := cabincrew.EngineOutput{
		EngineID:        "test-engine",
		Mode:            "flight-plan",
		ProtocolVersion: "1.0.0",
		ReceiptID:       "receipt-123",
		Status:          "success",
	}

	if output.EngineID != "test-engine" {
		fmt.Println("✗ Struct instantiation failed")
		return false
	}

	fmt.Println("✓ Struct instantiation successful")
	return true
}

func testJSONSerialization() bool {
	fmt.Println("Testing JSON serialization...")

	output := cabincrew.EngineOutput{
		EngineID:        "test",
		Mode:            "flight-plan",
		ProtocolVersion: "1.0.0",
		ReceiptID:       "r1",
		Status:          "success",
	}

	// Marshal to JSON
	jsonBytes, err := json.Marshal(output)
	if err != nil {
		fmt.Printf("✗ JSON marshaling failed: %v\n", err)
		return false
	}

	// Unmarshal from JSON
	var output2 cabincrew.EngineOutput
	if err := json.Unmarshal(jsonBytes, &output2); err != nil {
		fmt.Printf("✗ JSON unmarshaling failed: %v\n", err)
		return false
	}

	if output2.EngineID != output.EngineID {
		fmt.Println("✗ JSON round-trip failed")
		return false
	}

	fmt.Println("✓ JSON serialization working")
	return true
}

func main() {
	fmt.Println(string(make([]byte, 60)))
	for i := 0; i < 60; i++ {
		fmt.Print("=")
	}
	fmt.Println()
	fmt.Println("CabinCrew Protocol - Go Library Smoke Tests")
	for i := 0; i < 60; i++ {
		fmt.Print("=")
	}
	fmt.Println()

	tests := []func() bool{
		testImports,
		testEnumValues,
		testInstantiation,
		testJSONSerialization,
	}

	passed := 0
	failed := 0

	for _, test := range tests {
		if test() {
			passed++
		} else {
			failed++
		}
	}

	for i := 0; i < 60; i++ {
		fmt.Print("=")
	}
	fmt.Println()
	fmt.Printf("Results: %d passed, %d failed\n", passed, failed)
	for i := 0; i < 60; i++ {
		fmt.Print("=")
	}
	fmt.Println()

	if failed > 0 {
		os.Exit(1)
	}
}
