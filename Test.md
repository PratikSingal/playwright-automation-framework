Here's a refined version of your request, written so an AI agent can act on it directly:

---

**Goal:** Set up a scalable Playwright (TypeScript) automation framework that works with Playwright Test Agents (planner, generator, healer) and the Playwright MCP server.

**Part 1: Framework architecture**

Design a clean, reusable architecture with these layers:

1. **Central actions layer (`BaseActions` / `BasePage`)**: One class that wraps all common Playwright interactions (navigate, click, fill, select, check, hover, wait for visibility, get text, assert visible, assert URL/title, take screenshot). Every action should include built-in waits, consistent error messages, and logging. No test or page object should call raw Playwright APIs directly.
2. **Page Object Model (POM) layer**: One class per page that extends the base class. Each page object contains only locators (preferring `getByRole`, `getByLabel`, `getByTestId`) and page-specific methods built from the central actions.
3. **Fixtures layer**: Custom Playwright fixtures that create and inject page objects into tests, so tests never instantiate pages manually.
4. **Test layer**: Tests that read like business steps and contain no locators.
5. **Config and utilities**: `playwright.config.ts` with base URL, environment variables, retries, reporters (HTML and list), screenshots/video/trace on failure, plus helpers for test data and logging.

Provide the complete generic code for the base class, one sample page object, the fixtures file, one sample test, the config, and the recommended folder structure. Explain briefly how a new page should be added.

**Part 2: Reusable agent prompt for sanity tests**

Write a generic prompt I can reuse for any URL. When I provide a URL, the agent should:

1. Open the URL using the Playwright MCP server.
2. Explore the page and identify all visible elements, with a focus on forms: inputs, dropdowns, checkboxes, radio buttons, and buttons, plus key headings and links.
3. Generate a page object for that page that follows the architecture above, extends the base class, and uses stable, accessible locators.
4. Generate **sanity tests only**, which validate that:
   - the page loads successfully (URL, title, and a key heading or landmark are correct), and
   - every identified form element is visible (and enabled where applicable).
5. Not fill in or submit forms, and not test business logic or negative scenarios.
6. Run the tests, fix any failing locators (healer step), and report a summary of the elements found and the test results.

Prompt template:

```
Using the Playwright MCP server, open {URL}.
Explore the page and list all visible elements, focusing on form fields and buttons.
Create a page object named {PageName}Page in /pages that extends BasePage,
using getByRole / getByLabel / getByTestId locators and only BasePage actions.
Register it in fixtures/pages.fixture.ts.
Create /tests/sanity/{pageName}.sanity.spec.ts with sanity tests that check:
1) the page loads (URL, title, main heading), and
2) every form element is visible and enabled.
Do not fill or submit forms. Run the tests, fix any failing locators,
and give me a summary of the elements found and the test results.
```

---

If you'd like, I can also write the actual framework code (base class, sample POM, fixtures, config and folder structure) as files you can drop into your project.
