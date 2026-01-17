.PHONY: help w1-start w1-stop w1-clean w1-install w1-build site-start site-stop app-start app-stop app-install app-db-up app-db-down app-clean

# Variables
PROJECT_DIR := w1/project-alpha
BACKEND_DIR := $(PROJECT_DIR)/backend
FRONTEND_DIR := $(PROJECT_DIR)/frontend
PID_FILE := .pids

# App project variables (specs/my-w1/project-alpha)
APP_DIR := specs/my-w1/project-alpha
APP_BACKEND_DIR := $(APP_DIR)/backend
APP_FRONTEND_DIR := $(APP_DIR)/frontend
VENV_DIR := venv

help: ## Show this help message
	@echo "Project Alpha - Makefile Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'

w1-start: ## Start w1 project (backend + frontend preview)
	@echo "Starting Project Alpha..."
	@cd $(BACKEND_DIR) && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 & echo $$! > ../$(PID_FILE).backend
	@sleep 2
	@cd $(FRONTEND_DIR) && yarn preview --host 0.0.0.0 --port 5173 > /dev/null 2>&1 & echo $$! > ../$(PID_FILE).frontend
	@echo ""
	@echo "=========================================="
	@echo "Project Alpha is running!"
	@echo "=========================================="
	@echo "Backend PID: $$(cat $(PROJECT_DIR)/$(PID_FILE).backend 2>/dev/null || echo 'N/A')"
	@echo "Frontend PID: $$(cat $(PROJECT_DIR)/$(PID_FILE).frontend 2>/dev/null || echo 'N/A')"
	@echo ""
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/v1/docs"
	@echo ""
	@echo "Press Ctrl+C to stop, or run 'make w1-stop'"

w1-stop: ## Stop w1 project
	@echo "Stopping Project Alpha..."
	@# Stop backend by PID file
	@if [ -f $(PROJECT_DIR)/$(PID_FILE).backend ]; then \
		PID=$$(cat $(PROJECT_DIR)/$(PID_FILE).backend 2>/dev/null); \
		if [ -n "$$PID" ] && kill -0 $$PID 2>/dev/null; then \
			kill $$PID 2>/dev/null && echo "Backend stopped (PID: $$PID)" || echo "Failed to stop backend"; \
		else \
			echo "Backend process not running (PID file exists but process not found)"; \
		fi; \
		rm -f $(PROJECT_DIR)/$(PID_FILE).backend; \
	fi
	@# Stop frontend by PID file
	@if [ -f $(PROJECT_DIR)/$(PID_FILE).frontend ]; then \
		PID=$$(cat $(PROJECT_DIR)/$(PID_FILE).frontend 2>/dev/null); \
		if [ -n "$$PID" ] && kill -0 $$PID 2>/dev/null; then \
			kill $$PID 2>/dev/null && echo "Frontend stopped (PID: $$PID)" || echo "Failed to stop frontend"; \
		else \
			echo "Frontend process not running (PID file exists but process not found)"; \
		fi; \
		rm -f $(PROJECT_DIR)/$(PID_FILE).frontend; \
	fi
	@# Also kill processes by port (fallback - more reliable)
	@for PID in $$(lsof -ti:8000 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill $$PID 2>/dev/null && echo "Backend stopped by port 8000 (PID: $$PID)" || true; \
		fi; \
	done
	@for PID in $$(lsof -ti:5173 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill $$PID 2>/dev/null && echo "Frontend stopped by port 5173 (PID: $$PID)" || true; \
		fi; \
	done
	@# Wait a bit and force kill if still running
	@sleep 1
	@for PID in $$(lsof -ti:8000 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill -9 $$PID 2>/dev/null && echo "Backend force killed (PID: $$PID)" || true; \
		fi; \
	done
	@for PID in $$(lsof -ti:5173 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill -9 $$PID 2>/dev/null && echo "Frontend force killed (PID: $$PID)" || true; \
		fi; \
	done
	@echo "Done"

w1-install: ## Install all w1 dependencies
	@echo "Installing w1 backend dependencies..."
	@cd $(BACKEND_DIR) && uv sync
	@echo "Installing w1 frontend dependencies..."
	@cd $(FRONTEND_DIR) && yarn install

w1-build: ## Build w1 frontend for production
	@echo "Building w1 frontend..."
	@cd $(FRONTEND_DIR) && yarn build

site-start: ## Start site (Astro dev server)
	@echo "Starting Site..."
	@cd site && yarn dev --host 0.0.0.0 --port 4321 > /dev/null 2>&1 & echo $$! > ../$(PID_FILE).site
	@sleep 2
	@echo ""
	@echo "=========================================="
	@echo "Site is running!"
	@echo "=========================================="
	@echo "Site PID: $$(cat $(PID_FILE).site 2>/dev/null || echo 'N/A')"
	@echo ""
	@echo "Site: http://localhost:4321"
	@echo ""
	@echo "Press Ctrl+C to stop, or run 'make site-stop'"

site-stop: ## Stop site
	@echo "Stopping Site..."
	@# Stop site by PID file
	@if [ -f $(PID_FILE).site ]; then \
		PID=$$(cat $(PID_FILE).site 2>/dev/null); \
		if [ -n "$$PID" ] && kill -0 $$PID 2>/dev/null; then \
			kill $$PID 2>/dev/null && echo "Site stopped (PID: $$PID)" || echo "Failed to stop site"; \
		else \
			echo "Site process not running (PID file exists but process not found)"; \
		fi; \
		rm -f $(PID_FILE).site; \
	fi
	@# Also kill processes by port (fallback - more reliable)
	@for PID in $$(lsof -ti:4321 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill $$PID 2>/dev/null && echo "Site stopped by port 4321 (PID: $$PID)" || true; \
		fi; \
	done
	@# Wait a bit and force kill if still running
	@sleep 1
	@for PID in $$(lsof -ti:4321 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill -9 $$PID 2>/dev/null && echo "Site force killed (PID: $$PID)" || true; \
		fi; \
	done
	@echo "Done"

w1-clean: w1-stop ## Clean up w1 PID files and temporary files
	@echo "Cleaning up w1 project..."
	@rm -f $(PROJECT_DIR)/$(PID_FILE).backend $(PROJECT_DIR)/$(PID_FILE).frontend
	@echo "Done"

# App project commands (specs/my-w1/project-alpha)
app-db-up: ## Start PostgreSQL database for app
	@echo "Starting PostgreSQL database..."
	@cd $(APP_DIR) && docker-compose up -d postgres
	@echo "Waiting for database to be ready..."
	@sleep 3
	@cd $(APP_DIR) && docker-compose ps
	@echo "Database is ready!"

app-db-down: ## Stop PostgreSQL database for app
	@echo "Stopping PostgreSQL database..."
	@cd $(APP_DIR) && docker-compose down
	@echo "Database stopped"

app-install: ## Install all app dependencies
	@echo "Installing app backend dependencies..."
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi
	@echo "Activating virtual environment and installing dependencies..."
	@. $(VENV_DIR)/bin/activate && cd $(APP_BACKEND_DIR) && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Installing app frontend dependencies..."
	@cd $(APP_FRONTEND_DIR) && npm install
	@echo "All dependencies installed!"

app-start: app-db-up ## Start app (database + backend + frontend)
	@echo "Starting App (Project Alpha)..."
	@# Check if venv exists, create if not
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Virtual environment not found. Run 'make app-install' first."; \
		exit 1; \
	fi
	@# Start backend
	@echo "Starting backend..."
	@. $(VENV_DIR)/bin/activate && cd $(APP_BACKEND_DIR) && \
		uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 & \
		echo $$! > ../../../../$(PID_FILE).app-backend
	@sleep 2
	@# Start frontend
	@echo "Starting frontend..."
	@cd $(APP_FRONTEND_DIR) && \
		npm run dev -- --host 0.0.0.0 --port 5173 > /dev/null 2>&1 & \
		echo $$! > ../../../../$(PID_FILE).app-frontend
	@sleep 2
	@echo ""
	@echo "=========================================="
	@echo "App (Project Alpha) is running!"
	@echo "=========================================="
	@echo "Backend PID: $$(cat $(PID_FILE).app-backend 2>/dev/null || echo 'N/A')"
	@echo "Frontend PID: $$(cat $(PID_FILE).app-frontend 2>/dev/null || echo 'N/A')"
	@echo ""
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Press Ctrl+C to stop, or run 'make app-stop'"

app-stop: ## Stop app (backend + frontend, but not database)
	@echo "Stopping App (Project Alpha)..."
	@# Stop backend by PID file
	@if [ -f $(PID_FILE).app-backend ]; then \
		PID=$$(cat $(PID_FILE).app-backend 2>/dev/null); \
		if [ -n "$$PID" ] && kill -0 $$PID 2>/dev/null; then \
			kill $$PID 2>/dev/null && echo "Backend stopped (PID: $$PID)" || echo "Failed to stop backend"; \
		else \
			echo "Backend process not running (PID file exists but process not found)"; \
		fi; \
		rm -f $(PID_FILE).app-backend; \
	fi
	@# Stop frontend by PID file
	@if [ -f $(PID_FILE).app-frontend ]; then \
		PID=$$(cat $(PID_FILE).app-frontend 2>/dev/null); \
		if [ -n "$$PID" ] && kill -0 $$PID 2>/dev/null; then \
			kill $$PID 2>/dev/null && echo "Frontend stopped (PID: $$PID)" || echo "Failed to stop frontend"; \
		else \
			echo "Frontend process not running (PID file exists but process not found)"; \
		fi; \
		rm -f $(PID_FILE).app-frontend; \
	fi
	@# Also kill processes by port (fallback - more reliable)
	@for PID in $$(lsof -ti:8000 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill $$PID 2>/dev/null && echo "Backend stopped by port 8000 (PID: $$PID)" || true; \
		fi; \
	done
	@for PID in $$(lsof -ti:5173 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill $$PID 2>/dev/null && echo "Frontend stopped by port 5173 (PID: $$PID)" || true; \
		fi; \
	done
	@# Wait a bit and force kill if still running
	@sleep 1
	@for PID in $$(lsof -ti:8000 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill -9 $$PID 2>/dev/null && echo "Backend force killed (PID: $$PID)" || true; \
		fi; \
	done
	@for PID in $$(lsof -ti:5173 2>/dev/null); do \
		if [ -n "$$PID" ]; then \
			kill -9 $$PID 2>/dev/null && echo "Frontend force killed (PID: $$PID)" || true; \
		fi; \
	done
	@echo "Done"

app-clean: app-stop app-db-down ## Clean up app (stop all services and remove PID files)
	@echo "Cleaning up app project..."
	@rm -f $(PID_FILE).app-backend $(PID_FILE).app-frontend
	@echo "Done"
