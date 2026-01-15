-- Seed data for tickets and tags
-- This file can be executed with: psql -U postgres -d ticket_db -f seed.sql

-- Clear existing data (optional, comment out if you want to keep existing data)
-- TRUNCATE TABLE ticket_tags CASCADE;
-- TRUNCATE TABLE tickets CASCADE;
-- TRUNCATE TABLE tags CASCADE;
-- ALTER SEQUENCE tickets_id_seq RESTART WITH 1;
-- ALTER SEQUENCE tags_id_seq RESTART WITH 1;

-- Insert Tags
-- Platform tags
INSERT INTO tags (name, color, created_at) VALUES
('ios', '#007AFF', CURRENT_TIMESTAMP),
('android', '#3DDC84', CURRENT_TIMESTAMP),
('web', '#4285F4', CURRENT_TIMESTAMP),
('desktop', '#5865F2', CURRENT_TIMESTAMP),
('linux', '#FCC624', CURRENT_TIMESTAMP),
('windows', '#0078D4', CURRENT_TIMESTAMP),
('macos', '#000000', CURRENT_TIMESTAMP);

-- Project tags
INSERT INTO tags (name, color, created_at) VALUES
('viking', '#8B4513', CURRENT_TIMESTAMP),
('odin', '#1E3A8A', CURRENT_TIMESTAMP),
('thor', '#DC2626', CURRENT_TIMESTAMP),
('loki', '#059669', CURRENT_TIMESTAMP),
('valhalla', '#7C3AED', CURRENT_TIMESTAMP),
('ragnarok', '#B91C1C', CURRENT_TIMESTAMP);

-- Functional tags
INSERT INTO tags (name, color, created_at) VALUES
('autocomplete', '#10B981', CURRENT_TIMESTAMP),
('search', '#3B82F6', CURRENT_TIMESTAMP),
('authentication', '#EF4444', CURRENT_TIMESTAMP),
('authorization', '#F59E0B', CURRENT_TIMESTAMP),
('caching', '#8B5CF6', CURRENT_TIMESTAMP),
('database', '#06B6D4', CURRENT_TIMESTAMP),
('api', '#EC4899', CURRENT_TIMESTAMP),
('ui', '#F97316', CURRENT_TIMESTAMP),
('ux', '#14B8A6', CURRENT_TIMESTAMP),
('performance', '#6366F1', CURRENT_TIMESTAMP),
('security', '#DC2626', CURRENT_TIMESTAMP),
('testing', '#84CC16', CURRENT_TIMESTAMP),
('documentation', '#64748B', CURRENT_TIMESTAMP),
('refactoring', '#A855F7', CURRENT_TIMESTAMP),
('bugfix', '#EF4444', CURRENT_TIMESTAMP),
('feature', '#10B981', CURRENT_TIMESTAMP),
('enhancement', '#3B82F6', CURRENT_TIMESTAMP),
('optimization', '#F59E0B', CURRENT_TIMESTAMP),
('integration', '#8B5CF6', CURRENT_TIMESTAMP),
('migration', '#06B6D4', CURRENT_TIMESTAMP),
('monitoring', '#EC4899', CURRENT_TIMESTAMP),
('logging', '#F97316', CURRENT_TIMESTAMP),
('error-handling', '#DC2626', CURRENT_TIMESTAMP),
('validation', '#14B8A6', CURRENT_TIMESTAMP),
('notification', '#6366F1', CURRENT_TIMESTAMP),
('analytics', '#84CC16', CURRENT_TIMESTAMP),
('backup', '#64748B', CURRENT_TIMESTAMP),
('deployment', '#A855F7', CURRENT_TIMESTAMP);

-- Priority/Status tags
INSERT INTO tags (name, color, created_at) VALUES
('high-priority', '#DC2626', CURRENT_TIMESTAMP),
('medium-priority', '#F59E0B', CURRENT_TIMESTAMP),
('low-priority', '#10B981', CURRENT_TIMESTAMP),
('blocked', '#64748B', CURRENT_TIMESTAMP),
('in-progress', '#3B82F6', CURRENT_TIMESTAMP);

-- Insert Tickets (50 meaningful tickets)
INSERT INTO tickets (title, description, status, created_at, updated_at, completed_at) VALUES
-- Completed tickets
('Implement user authentication system', 'Build a secure authentication system with JWT tokens, password hashing, and session management. Include support for email/password and OAuth providers.', 'completed', CURRENT_TIMESTAMP - INTERVAL '30 days', CURRENT_TIMESTAMP - INTERVAL '25 days', CURRENT_TIMESTAMP - INTERVAL '25 days'),
('Add autocomplete to search bar', 'Implement autocomplete functionality for the main search bar with suggestions based on user history and popular queries.', 'completed', CURRENT_TIMESTAMP - INTERVAL '28 days', CURRENT_TIMESTAMP - INTERVAL '22 days', CURRENT_TIMESTAMP - INTERVAL '22 days'),
('Optimize database query performance', 'Review and optimize slow database queries, add proper indexes, and implement query caching for frequently accessed data.', 'completed', CURRENT_TIMESTAMP - INTERVAL '25 days', CURRENT_TIMESTAMP - INTERVAL '20 days', CURRENT_TIMESTAMP - INTERVAL '20 days'),
('Create API documentation', 'Generate comprehensive API documentation using OpenAPI/Swagger with examples, request/response schemas, and authentication details.', 'completed', CURRENT_TIMESTAMP - INTERVAL '22 days', CURRENT_TIMESTAMP - INTERVAL '18 days', CURRENT_TIMESTAMP - INTERVAL '18 days'),
('Implement error logging system', 'Set up centralized error logging with proper categorization, alerting, and integration with monitoring tools.', 'completed', CURRENT_TIMESTAMP - INTERVAL '20 days', CURRENT_TIMESTAMP - INTERVAL '15 days', CURRENT_TIMESTAMP - INTERVAL '15 days'),
('Add unit tests for core modules', 'Write comprehensive unit tests for authentication, database operations, and API endpoints with >80% code coverage.', 'completed', CURRENT_TIMESTAMP - INTERVAL '18 days', CURRENT_TIMESTAMP - INTERVAL '12 days', CURRENT_TIMESTAMP - INTERVAL '12 days'),
('Design responsive UI for mobile devices', 'Create mobile-responsive layouts for all major pages, ensuring proper touch interactions and optimal viewing on small screens.', 'completed', CURRENT_TIMESTAMP - INTERVAL '15 days', CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP - INTERVAL '10 days'),
('Implement user role-based access control', 'Add role-based authorization system with admin, moderator, and user roles, including permission checks for all endpoints.', 'completed', CURRENT_TIMESTAMP - INTERVAL '12 days', CURRENT_TIMESTAMP - INTERVAL '8 days', CURRENT_TIMESTAMP - INTERVAL '8 days'),
('Set up CI/CD pipeline', 'Configure continuous integration and deployment pipeline with automated testing, code quality checks, and staging/production deployments.', 'completed', CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP - INTERVAL '5 days'),
('Add data validation for user inputs', 'Implement comprehensive input validation on both frontend and backend to prevent invalid data and security vulnerabilities.', 'completed', CURRENT_TIMESTAMP - INTERVAL '8 days', CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP - INTERVAL '3 days'),

-- Pending tickets
('Implement real-time notifications', 'Build a notification system that sends real-time updates to users via WebSocket connections for important events and messages.', 'pending', CURRENT_TIMESTAMP - INTERVAL '7 days', CURRENT_TIMESTAMP - INTERVAL '7 days', NULL),
('Add advanced search filters', 'Enhance search functionality with multiple filter options including date range, category, status, and custom tags.', 'pending', CURRENT_TIMESTAMP - INTERVAL '6 days', CURRENT_TIMESTAMP - INTERVAL '6 days', NULL),
('Create iOS mobile application', 'Develop native iOS app using Swift with core features including authentication, data synchronization, and offline support.', 'pending', CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP - INTERVAL '5 days', NULL),
('Implement data analytics dashboard', 'Build an analytics dashboard showing user engagement metrics, system performance, and business KPIs with interactive charts.', 'pending', CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP - INTERVAL '5 days', NULL),
('Add multi-language support', 'Implement internationalization (i18n) system supporting English, Spanish, French, and Chinese with dynamic language switching.', 'pending', CURRENT_TIMESTAMP - INTERVAL '4 days', CURRENT_TIMESTAMP - INTERVAL '4 days', NULL),
('Optimize frontend bundle size', 'Analyze and reduce JavaScript bundle size through code splitting, lazy loading, and removing unused dependencies.', 'pending', CURRENT_TIMESTAMP - INTERVAL '4 days', CURRENT_TIMESTAMP - INTERVAL '4 days', NULL),
('Implement file upload functionality', 'Add secure file upload feature with support for images, documents, and media files with size limits and virus scanning.', 'pending', CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP - INTERVAL '3 days', NULL),
('Create automated backup system', 'Set up automated daily backups for database and file storage with retention policies and disaster recovery procedures.', 'pending', CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP - INTERVAL '3 days', NULL),
('Add user profile management', 'Build comprehensive user profile pages with editable information, avatar upload, preferences, and activity history.', 'pending', CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days', NULL),
('Implement rate limiting', 'Add rate limiting middleware to prevent API abuse and ensure fair usage across all endpoints with configurable limits.', 'pending', CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days', NULL),
('Create Android mobile application', 'Develop native Android app using Kotlin with Material Design, offline capabilities, and push notifications.', 'pending', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day', NULL),
('Add comment and discussion system', 'Implement threaded comments system with replies, reactions, moderation tools, and real-time updates.', 'pending', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day', NULL),
('Implement dark mode theme', 'Add dark mode support across the entire application with user preference storage and automatic system detection.', 'pending', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day', NULL),
('Add email notification system', 'Set up email service integration for sending transactional emails, notifications, and marketing campaigns.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create admin dashboard', 'Build comprehensive admin dashboard for managing users, content, system settings, and viewing analytics.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement content moderation tools', 'Add automated and manual content moderation features including keyword filtering, spam detection, and review workflows.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add social media integration', 'Integrate with major social media platforms for login, sharing, and importing user data with proper OAuth flows.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Optimize image loading and storage', 'Implement image optimization, lazy loading, CDN integration, and efficient storage solutions for better performance.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create API rate limit dashboard', 'Build monitoring dashboard for tracking API usage, rate limit violations, and identifying potential abuse patterns.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement two-factor authentication', 'Add 2FA support using TOTP authenticator apps and SMS verification for enhanced account security.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add export functionality', 'Implement data export features allowing users to download their data in various formats (JSON, CSV, PDF).', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create user onboarding flow', 'Design and implement interactive onboarding experience for new users with tutorials and feature highlights.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement activity feed', 'Build activity feed showing user actions, system events, and updates in chronological order with filtering options.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add keyboard shortcuts', 'Implement keyboard shortcuts for common actions to improve productivity and accessibility for power users.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create custom reporting system', 'Build flexible reporting system allowing users to create custom reports with filters, grouping, and export options.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement audit logging', 'Add comprehensive audit logging for all critical operations including user actions, data changes, and system events.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add drag-and-drop interface', 'Implement drag-and-drop functionality for file uploads, list reordering, and visual workflow builders.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create help center and FAQ', 'Build comprehensive help center with searchable articles, FAQ section, and interactive tutorials.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement advanced caching strategy', 'Add multi-layer caching system using Redis for session data, query results, and frequently accessed content.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add calendar and scheduling features', 'Implement calendar view with event scheduling, reminders, and integration with external calendar services.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create data visualization components', 'Build reusable chart and graph components for displaying analytics data with interactive features.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement webhook system', 'Add webhook support for external integrations allowing third-party services to receive real-time event notifications.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add accessibility improvements', 'Enhance accessibility with ARIA labels, keyboard navigation, screen reader support, and WCAG 2.1 compliance.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create mobile app for desktop platform', 'Develop cross-platform desktop application using Electron with native OS integration and offline capabilities.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement advanced search with AI', 'Add AI-powered search with natural language processing, semantic search, and intelligent result ranking.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add collaboration features', 'Implement real-time collaboration tools including shared workspaces, co-editing, and presence indicators.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create automated testing suite', 'Set up comprehensive end-to-end testing framework with automated browser testing and API integration tests.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement payment integration', 'Add payment processing integration with support for multiple payment methods and subscription management.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add version control for content', 'Implement version history and rollback functionality for user-generated content with diff visualization.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create mobile-responsive navigation', 'Redesign navigation menu for mobile devices with hamburger menu, bottom navigation, and gesture support.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement data migration tools', 'Build tools for migrating data between environments, handling schema changes, and data transformation.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add performance monitoring', 'Integrate application performance monitoring (APM) tools for tracking response times, error rates, and system health.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create user feedback system', 'Implement feedback collection system with surveys, ratings, and feature request tracking with voting mechanism.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Implement single sign-on (SSO)', 'Add SSO support using SAML and OAuth protocols for enterprise customers with multiple identity providers.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Add geolocation features', 'Implement location-based features including geofencing, location search, and mapping integration.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Create automated deployment scripts', 'Build deployment automation scripts for zero-downtime deployments with rollback capabilities and health checks.', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL);

-- Link tickets to tags (ticket_tags associations)
-- Ticket 1: authentication, api, security, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(1, (SELECT id FROM tags WHERE name = 'authentication'), CURRENT_TIMESTAMP),
(1, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP),
(1, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(1, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 2: autocomplete, search, ui, ux, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(2, (SELECT id FROM tags WHERE name = 'autocomplete'), CURRENT_TIMESTAMP),
(2, (SELECT id FROM tags WHERE name = 'search'), CURRENT_TIMESTAMP),
(2, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(2, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(2, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 3: database, performance, optimization
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(3, (SELECT id FROM tags WHERE name = 'database'), CURRENT_TIMESTAMP),
(3, (SELECT id FROM tags WHERE name = 'performance'), CURRENT_TIMESTAMP),
(3, (SELECT id FROM tags WHERE name = 'optimization'), CURRENT_TIMESTAMP);

-- Ticket 4: documentation, api
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(4, (SELECT id FROM tags WHERE name = 'documentation'), CURRENT_TIMESTAMP),
(4, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP);

-- Ticket 5: logging, monitoring, error-handling
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(5, (SELECT id FROM tags WHERE name = 'logging'), CURRENT_TIMESTAMP),
(5, (SELECT id FROM tags WHERE name = 'monitoring'), CURRENT_TIMESTAMP),
(5, (SELECT id FROM tags WHERE name = 'error-handling'), CURRENT_TIMESTAMP);

-- Ticket 6: testing
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(6, (SELECT id FROM tags WHERE name = 'testing'), CURRENT_TIMESTAMP);

-- Ticket 7: ui, ux, ios, android, web
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(7, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(7, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(7, (SELECT id FROM tags WHERE name = 'ios'), CURRENT_TIMESTAMP),
(7, (SELECT id FROM tags WHERE name = 'android'), CURRENT_TIMESTAMP),
(7, (SELECT id FROM tags WHERE name = 'web'), CURRENT_TIMESTAMP);

-- Ticket 8: authorization, security, authentication, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(8, (SELECT id FROM tags WHERE name = 'authorization'), CURRENT_TIMESTAMP),
(8, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(8, (SELECT id FROM tags WHERE name = 'authentication'), CURRENT_TIMESTAMP),
(8, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 9: deployment
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(9, (SELECT id FROM tags WHERE name = 'deployment'), CURRENT_TIMESTAMP);

-- Ticket 10: validation, security
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(10, (SELECT id FROM tags WHERE name = 'validation'), CURRENT_TIMESTAMP),
(10, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP);

-- Ticket 11: notification, api, feature, high-priority
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(11, (SELECT id FROM tags WHERE name = 'notification'), CURRENT_TIMESTAMP),
(11, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP),
(11, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(11, (SELECT id FROM tags WHERE name = 'high-priority'), CURRENT_TIMESTAMP);

-- Ticket 12: search, ui, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(12, (SELECT id FROM tags WHERE name = 'search'), CURRENT_TIMESTAMP),
(12, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(12, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 13: ios, feature, high-priority, viking
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(13, (SELECT id FROM tags WHERE name = 'ios'), CURRENT_TIMESTAMP),
(13, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(13, (SELECT id FROM tags WHERE name = 'high-priority'), CURRENT_TIMESTAMP),
(13, (SELECT id FROM tags WHERE name = 'viking'), CURRENT_TIMESTAMP);

-- Ticket 14: analytics, monitoring, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(14, (SELECT id FROM tags WHERE name = 'analytics'), CURRENT_TIMESTAMP),
(14, (SELECT id FROM tags WHERE name = 'monitoring'), CURRENT_TIMESTAMP),
(14, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 15: ui, ux, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(15, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(15, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(15, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 16: performance, optimization, web
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(16, (SELECT id FROM tags WHERE name = 'performance'), CURRENT_TIMESTAMP),
(16, (SELECT id FROM tags WHERE name = 'optimization'), CURRENT_TIMESTAMP),
(16, (SELECT id FROM tags WHERE name = 'web'), CURRENT_TIMESTAMP);

-- Ticket 17: api, security, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(17, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP),
(17, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(17, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 18: backup, database, high-priority
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(18, (SELECT id FROM tags WHERE name = 'backup'), CURRENT_TIMESTAMP),
(18, (SELECT id FROM tags WHERE name = 'database'), CURRENT_TIMESTAMP),
(18, (SELECT id FROM tags WHERE name = 'high-priority'), CURRENT_TIMESTAMP);

-- Ticket 19: ui, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(19, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(19, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 20: api, security, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(20, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP),
(20, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(20, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 21: android, feature, high-priority, viking
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(21, (SELECT id FROM tags WHERE name = 'android'), CURRENT_TIMESTAMP),
(21, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(21, (SELECT id FROM tags WHERE name = 'high-priority'), CURRENT_TIMESTAMP),
(21, (SELECT id FROM tags WHERE name = 'viking'), CURRENT_TIMESTAMP);

-- Ticket 22: feature, api
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(22, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(22, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP);

-- Ticket 23: ui, ux, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(23, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(23, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(23, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 24: notification, integration, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(24, (SELECT id FROM tags WHERE name = 'notification'), CURRENT_TIMESTAMP),
(24, (SELECT id FROM tags WHERE name = 'integration'), CURRENT_TIMESTAMP),
(24, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 25: feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(25, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 26: security, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(26, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(26, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 27: integration, api, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(27, (SELECT id FROM tags WHERE name = 'integration'), CURRENT_TIMESTAMP),
(27, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP),
(27, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 28: performance, optimization, web
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(28, (SELECT id FROM tags WHERE name = 'performance'), CURRENT_TIMESTAMP),
(28, (SELECT id FROM tags WHERE name = 'optimization'), CURRENT_TIMESTAMP),
(28, (SELECT id FROM tags WHERE name = 'web'), CURRENT_TIMESTAMP);

-- Ticket 29: security, authentication, feature, high-priority
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(29, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(29, (SELECT id FROM tags WHERE name = 'authentication'), CURRENT_TIMESTAMP),
(29, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(29, (SELECT id FROM tags WHERE name = 'high-priority'), CURRENT_TIMESTAMP);

-- Ticket 30: feature, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(30, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(30, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 31: ui, ux, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(31, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(31, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(31, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 32: ui, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(32, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(32, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 33: feature, analytics
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(33, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(33, (SELECT id FROM tags WHERE name = 'analytics'), CURRENT_TIMESTAMP);

-- Ticket 34: api, integration, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(34, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP),
(34, (SELECT id FROM tags WHERE name = 'integration'), CURRENT_TIMESTAMP),
(34, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 35: ui, ux, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(35, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(35, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(35, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 36: desktop, feature, viking
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(36, (SELECT id FROM tags WHERE name = 'desktop'), CURRENT_TIMESTAMP),
(36, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(36, (SELECT id FROM tags WHERE name = 'viking'), CURRENT_TIMESTAMP);

-- Ticket 37: search, enhancement, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(37, (SELECT id FROM tags WHERE name = 'search'), CURRENT_TIMESTAMP),
(37, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP),
(37, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 38: feature, api
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(38, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(38, (SELECT id FROM tags WHERE name = 'api'), CURRENT_TIMESTAMP);

-- Ticket 39: testing, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(39, (SELECT id FROM tags WHERE name = 'testing'), CURRENT_TIMESTAMP),
(39, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 40: integration, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(40, (SELECT id FROM tags WHERE name = 'integration'), CURRENT_TIMESTAMP),
(40, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 41: feature, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(41, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(41, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 42: security, authentication, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(42, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(42, (SELECT id FROM tags WHERE name = 'authentication'), CURRENT_TIMESTAMP),
(42, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 43: feature, integration
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(43, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(43, (SELECT id FROM tags WHERE name = 'integration'), CURRENT_TIMESTAMP);

-- Ticket 44: ui, ux, ios, android, web, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(44, (SELECT id FROM tags WHERE name = 'ui'), CURRENT_TIMESTAMP),
(44, (SELECT id FROM tags WHERE name = 'ux'), CURRENT_TIMESTAMP),
(44, (SELECT id FROM tags WHERE name = 'ios'), CURRENT_TIMESTAMP),
(44, (SELECT id FROM tags WHERE name = 'android'), CURRENT_TIMESTAMP),
(44, (SELECT id FROM tags WHERE name = 'web'), CURRENT_TIMESTAMP),
(44, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 45: migration, database, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(45, (SELECT id FROM tags WHERE name = 'migration'), CURRENT_TIMESTAMP),
(45, (SELECT id FROM tags WHERE name = 'database'), CURRENT_TIMESTAMP),
(45, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 46: monitoring, performance, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(46, (SELECT id FROM tags WHERE name = 'monitoring'), CURRENT_TIMESTAMP),
(46, (SELECT id FROM tags WHERE name = 'performance'), CURRENT_TIMESTAMP),
(46, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 47: feature, enhancement
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(47, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(47, (SELECT id FROM tags WHERE name = 'enhancement'), CURRENT_TIMESTAMP);

-- Ticket 48: security, authentication, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(48, (SELECT id FROM tags WHERE name = 'security'), CURRENT_TIMESTAMP),
(48, (SELECT id FROM tags WHERE name = 'authentication'), CURRENT_TIMESTAMP),
(48, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);

-- Ticket 49: feature, integration
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(49, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP),
(49, (SELECT id FROM tags WHERE name = 'integration'), CURRENT_TIMESTAMP);

-- Ticket 50: deployment, feature
INSERT INTO ticket_tags (ticket_id, tag_id, created_at) VALUES
(50, (SELECT id FROM tags WHERE name = 'deployment'), CURRENT_TIMESTAMP),
(50, (SELECT id FROM tags WHERE name = 'feature'), CURRENT_TIMESTAMP);
