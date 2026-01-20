#!/bin/bash

# E2E Test Script for Project Alpha
# This script tests the full integration between frontend and backend

set -e

echo "🚀 Starting E2E Tests for Project Alpha"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:5173"
MAX_RETRIES=30
RETRY_DELAY=2

# Function to check if a service is running
check_service() {
    local url=$1
    local service_name=$2
    
    echo -e "${YELLOW}Checking if ${service_name} is running at ${url}...${NC}"
    
    for i in $(seq 1 $MAX_RETRIES); do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ ${service_name} is running${NC}"
            return 0
        fi
        echo -e "${YELLOW}Waiting for ${service_name}... (${i}/${MAX_RETRIES})${NC}"
        sleep $RETRY_DELAY
    done
    
    echo -e "${RED}✗ ${service_name} is not running after ${MAX_RETRIES} attempts${NC}"
    return 1
}

# Check backend health
if ! check_service "${BACKEND_URL}/health" "Backend"; then
    echo -e "${RED}Backend is not running. Please start it first:${NC}"
    echo "  cd backend && uvicorn app.main:app --reload"
    exit 1
fi

# Check frontend
if ! check_service "${FRONTEND_URL}" "Frontend"; then
    echo -e "${YELLOW}Frontend is not running. Starting tests with backend only...${NC}"
fi

echo ""
echo "🧪 Running API Tests"
echo "===================="

# Test 1: Health check
echo -e "\n${YELLOW}Test 1: Health Check${NC}"
HEALTH_RESPONSE=$(curl -s "${BACKEND_URL}/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi

# Test 2: Create Tag
echo -e "\n${YELLOW}Test 2: Create Tag${NC}"
TAG_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/v1/tags/" \
    -H "Content-Type: application/json" \
    -d '{"name": "e2e-test-tag", "color": "#FF0000"}')
TAG_ID=$(echo "$TAG_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ -n "$TAG_ID" ]; then
    echo -e "${GREEN}✓ Tag created with ID: ${TAG_ID}${NC}"
else
    echo -e "${RED}✗ Failed to create tag${NC}"
    echo "Response: $TAG_RESPONSE"
    exit 1
fi

# Test 3: Create Ticket
echo -e "\n${YELLOW}Test 3: Create Ticket${NC}"
TICKET_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/v1/tickets/" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"E2E Test Ticket\", \"description\": \"This is an E2E test ticket\", \"tag_ids\": [${TAG_ID}]}")
TICKET_ID=$(echo "$TICKET_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ -n "$TICKET_ID" ]; then
    echo -e "${GREEN}✓ Ticket created with ID: ${TICKET_ID}${NC}"
else
    echo -e "${RED}✗ Failed to create ticket${NC}"
    echo "Response: $TICKET_RESPONSE"
    exit 1
fi

# Test 4: Get Ticket
echo -e "\n${YELLOW}Test 4: Get Ticket${NC}"
GET_TICKET_RESPONSE=$(curl -s "${BACKEND_URL}/api/v1/tickets/${TICKET_ID}")
if echo "$GET_TICKET_RESPONSE" | grep -q "E2E Test Ticket"; then
    echo -e "${GREEN}✓ Ticket retrieved successfully${NC}"
else
    echo -e "${RED}✗ Failed to retrieve ticket${NC}"
    exit 1
fi

# Test 5: Complete Ticket
echo -e "\n${YELLOW}Test 5: Complete Ticket${NC}"
COMPLETE_RESPONSE=$(curl -s -X PATCH "${BACKEND_URL}/api/v1/tickets/${TICKET_ID}/complete")
if echo "$COMPLETE_RESPONSE" | grep -q '"status":"completed"'; then
    echo -e "${GREEN}✓ Ticket completed successfully${NC}"
else
    echo -e "${RED}✗ Failed to complete ticket${NC}"
    exit 1
fi

# Test 6: Search Tickets
echo -e "\n${YELLOW}Test 6: Search Tickets${NC}"
SEARCH_RESPONSE=$(curl -s "${BACKEND_URL}/api/v1/tickets/?search=E2E")
if echo "$SEARCH_RESPONSE" | grep -q "E2E Test Ticket"; then
    echo -e "${GREEN}✓ Search works correctly${NC}"
else
    echo -e "${RED}✗ Search failed${NC}"
    exit 1
fi

# Test 7: Filter by Status
echo -e "\n${YELLOW}Test 7: Filter by Status${NC}"
FILTER_RESPONSE=$(curl -s "${BACKEND_URL}/api/v1/tickets/?status=completed")
if echo "$FILTER_RESPONSE" | grep -q "E2E Test Ticket"; then
    echo -e "${GREEN}✓ Status filter works correctly${NC}"
else
    echo -e "${RED}✗ Status filter failed${NC}"
    exit 1
fi

# Test 8: Update Ticket
echo -e "\n${YELLOW}Test 8: Update Ticket${NC}"
UPDATE_RESPONSE=$(curl -s -X PUT "${BACKEND_URL}/api/v1/tickets/${TICKET_ID}" \
    -H "Content-Type: application/json" \
    -d '{"title": "E2E Test Ticket - Updated", "description": "Updated description"}')
if echo "$UPDATE_RESPONSE" | grep -q "E2E Test Ticket - Updated"; then
    echo -e "${GREEN}✓ Ticket updated successfully${NC}"
else
    echo -e "${RED}✗ Failed to update ticket${NC}"
    exit 1
fi

# Test 9: Delete Ticket
echo -e "\n${YELLOW}Test 9: Delete Ticket${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "${BACKEND_URL}/api/v1/tickets/${TICKET_ID}" -w "%{http_code}")
HTTP_CODE=$(echo "$DELETE_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "204" ]; then
    echo -e "${GREEN}✓ Ticket deleted successfully${NC}"
else
    echo -e "${RED}✗ Failed to delete ticket (HTTP ${HTTP_CODE})${NC}"
    exit 1
fi

# Test 10: Delete Tag
echo -e "\n${YELLOW}Test 10: Delete Tag${NC}"
DELETE_TAG_RESPONSE=$(curl -s -X DELETE "${BACKEND_URL}/api/v1/tags/${TAG_ID}" -w "%{http_code}")
HTTP_CODE=$(echo "$DELETE_TAG_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "204" ]; then
    echo -e "${GREEN}✓ Tag deleted successfully${NC}"
else
    echo -e "${RED}✗ Failed to delete tag (HTTP ${HTTP_CODE})${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ All E2E Tests Passed!${NC}"
echo -e "${GREEN}========================================${NC}"
