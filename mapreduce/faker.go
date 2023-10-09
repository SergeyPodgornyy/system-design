package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"math/rand"
	"os"
	"time"

	"github.com/jaswdr/faker"
)

// go run faker.go -output=hosts/europe/people.csv -records=200
// go run faker.go -output=hosts/america/people.csv -records=200
// go run faker.go -output=hosts/asia/people.csv -records=200
// go run faker.go -output=hosts/africa/people.csv -records=200
func main() {
	// Define command-line flags
	outputFile := flag.String("output", "random_data.csv", "Output CSV file name")
	numRecords := flag.Int("records", 100, "Number of records to generate")
	flag.Parse()

	// Create a CSV file
	file, err := os.Create(*outputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Create a CSV writer
	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write the CSV header
	header := []string{"Name", "Birthdate"}
	writer.Write(header)

	// Create a Faker generator
	fake := faker.New()

	// Generate random names and birthdates and write to CSV
	for i := 0; i < *numRecords; i++ {
		name := fake.Person().Name()
		birthdate := generateRandomBirthdate()
		record := []string{name, birthdate}
		writer.Write(record)
	}

	fmt.Printf("Generated %d records and saved to %s\n", *numRecords, *outputFile)
}

func generateRandomBirthdate() string {
	min := time.Date(1950, 1, 1, 0, 0, 0, 0, time.UTC).Unix()
	max := time.Now().Unix()
	randomUnix := min + rand.Int63n(max-min)
	randomDate := time.Unix(randomUnix, 0)
	return randomDate.Format("2006-01-02")
}
