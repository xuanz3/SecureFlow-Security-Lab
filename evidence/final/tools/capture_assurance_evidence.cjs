const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

function launchOptions() {
  const channel = process.env.SECUREFLOW_BROWSER_CHANNEL || "chrome";
  const executablePath = process.env.SECUREFLOW_BROWSER_EXECUTABLE || "";

  const options = { headless: true };
  if (executablePath) {
    options.executablePath = executablePath;
  } else {
    options.channel = channel;
  }
  return options;
}

async function main() {
  const [appUrl, pagesDir, outputDir] = process.argv.slice(2);
  if (!appUrl || !pagesDir || !outputDir) {
    throw new Error("Usage: capture_assurance_evidence.cjs <app-url> <pages-dir> <output-dir>");
  }

  fs.mkdirSync(outputDir, { recursive: true });

  const cases = [
    {
      url: appUrl,
      file: "01-application-overview.png",
      selectors: [
        "text=SecureFlow Security Lab",
        "text=34 automated tests",
        "text=Governance and recovery",
      ],
    },
    {
      url: pathToFileURL(path.join(pagesDir, "02-security-pipeline.html")).href,
      file: "02-security-pipeline.png",
      selectors: ["text=Security pipeline", "text=Pull request assurance path"],
    },
    {
      url: pathToFileURL(path.join(pagesDir, "03-assessment-findings.html")).href,
      file: "03-assessment-findings.png",
      selectors: ["text=Assessment findings", "text=PH4-F08"],
    },
    {
      url: pathToFileURL(path.join(pagesDir, "04-remediation-retest.html")).href,
      file: "04-remediation-retest.png",
      selectors: ["text=Remediation and retest", "text=8 / 8"],
    },
    {
      url: pathToFileURL(path.join(pagesDir, "05-detection-investigation.html")).href,
      file: "05-detection-investigation.png",
      selectors: ["text=Detection investigation", "text=5 / 5"],
    },
    {
      url: pathToFileURL(path.join(pagesDir, "06-governance-recovery.html")).href,
      file: "06-governance-recovery.png",
      selectors: ["text=Governance and recovery", "text=5.007s"],
    },
  ];

  const browser = await chromium.launch(launchOptions());
  console.log(`Capture browser: ${browser.version()}`);

  const context = await browser.newContext({
    viewport: { width: 1600, height: 900 },
    deviceScaleFactor: 1,
    locale: "en-AU",
    timezoneId: "Australia/Melbourne",
    reducedMotion: "reduce",
  });

  try {
    for (const item of cases) {
      const page = await context.newPage();
      await page.goto(item.url, {
        waitUntil: item.url.startsWith("file:") ? "load" : "networkidle",
        timeout: 60000,
      });
      await page.evaluate(async () => {
        if (document.fonts && document.fonts.ready) {
          await document.fonts.ready;
        }
      });
      for (const selector of item.selectors) {
        await page.locator(selector).first().waitFor({
          state: "visible",
          timeout: 15000,
        });
      }
      await page.screenshot({
        path: path.join(outputDir, item.file),
        type: "png",
        fullPage: false,
        animations: "disabled",
      });
      await page.close();
      console.log(`Captured ${item.file}`);
    }
  } finally {
    await context.close();
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
