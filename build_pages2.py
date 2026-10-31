"""Content pages 2-7. Run: python build_pages2.py"""

from build_site import simple_page, page, write

# ======================================================================
# Etsy fees 2026
# ======================================================================
FEES_BODY = """
<p class="lede">Every fee Etsy charges a US seller in 2026, in one place, with the real-world example that
shows how much of a $35 order actually reaches you.</p>

<h2>The five fees on a normal sale</h2>
<table style="border-collapse:collapse;width:100%;max-width:680px;font-size:0.95rem">
  <tr style="border-bottom:1px solid #e5e7eb;text-align:left">
    <th style="padding:8px">Fee</th><th style="padding:8px">Rate</th><th style="padding:8px">Charged on</th>
  </tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Listing fee</td><td style="padding:8px">$0.20</td>
    <td style="padding:8px">Every listing, every 4 months, and again on renewal</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Transaction fee</td><td style="padding:8px">6.5%</td>
    <td style="padding:8px">Item price + shipping + gift wrap</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Payment processing</td><td style="padding:8px">3% + $0.25 <span class="muted small">(US)</span></td>
    <td style="padding:8px">Total payment collected</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Regulatory operating fee</td><td style="padding:8px">country-specific %</td>
    <td style="padding:8px">Item price — varies by seller location and has changed several times</td></tr>
  <tr>
    <td style="padding:8px">Off-site ads</td><td style="padding:8px">15% or 12%</td>
    <td style="padding:8px">Only on sales that arrive through an off-site ad</td></tr>
</table>

<h2>Off-site ads: the one that decides your margin</h2>
<p>Sellers making under $10,000 per year can opt out of off-site ads. Sellers above that threshold are in the
program permanently. When a sale is attributed to an off-site ad, Etsy takes <strong>15% of the item price plus
shipping</strong> — the single largest fee on most orders. Sellers above the threshold pay 12% instead.</p>
<p>You do not choose which sales get the fee; Etsy attributes them. That means your yearly ad cost is partly
luck, and it is why you should model the worst case (15%) rather than the average case.</p>

<h2>Worked example, 2026 rates</h2>
<p>$35 item, buyer pays $5.99 shipping, item cost $10, 3% Etsy Ads, one off-site ad sale:</p>
<table style="border-collapse:collapse;width:100%;max-width:560px">
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Buyer pays</td><td style="text-align:right;padding:6px 8px">$40.99</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Transaction fee 6.5%</td><td style="text-align:right;padding:6px 8px">−$2.27</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Processing 3% + $0.25</td><td style="text-align:right;padding:6px 8px">−$1.48</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Listing fee</td><td style="text-align:right;padding:6px 8px">−$0.20</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Regulatory 0.25%</td><td style="text-align:right;padding:6px 8px">−$0.09</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Etsy Ads 3%</td><td style="text-align:right;padding:6px 8px">−$1.23</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Off-site ads 15%</td><td style="text-align:right;padding:6px 8px">−$6.15</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb"><td style="padding:6px 8px">Item cost</td><td style="text-align:right;padding:6px 8px">−$10.00</td></tr>
  <tr><td style="padding:6px 8px"><strong>You keep</strong></td><td style="text-align:right;padding:6px 8px"><strong>$19.57</strong>
  <span class="small muted">(47.7% margin)</span></td></tr>
</table>
<p style="margin-top:12px">Fees alone took $11.42 — 28% of the buyer's payment — before the product cost. Run your
own numbers in the <a href="/tools/marketplace-fee-calculator.html">marketplace fee calculator</a>.</p>

<h2>Three fees most sellers forget</h2>
<ul>
  <li><strong>Shipping is not fee-free.</strong> The transaction fee and processing fee both apply to the shipping
amount the buyer pays. If you charge exact postage, you still lose a percentage of it.</li>
  <li><strong>Currency conversion.</strong> Selling in a currency other than your payout currency adds a conversion
cost on top of the listed fees — it does not show up as an Etsy fee line, but it reduces your deposit.</li>
  <li><strong>Auto-renew.</strong> A listing renews every 4 months (and relists after each sale) at $0.20. With
  100 live listings that is $20 every 4 months whether or not anything sells.</li>
</ul>

<h2>How to keep more of each sale</h2>
<ol>
  <li><strong>Price on net, not gross.</strong> Decide the profit you want, then solve for price — the
  calculator's “price for a 30% margin” does this for you.</li>
  <li><strong>Raise price instead of eating the ad fee.</strong> A $5 price increase on a $35 item more than covers
  the 15% off-site fee on that order.</li>
  <li><strong>Keep a fee log.</strong> Etsy changes fees and the regulatory fee has moved more than once. One table
  with the date you last checked keeps your pricing honest.</li>
</ol>
<div class="promo">
  <strong>Track it automatically:</strong> the <a href="/profit-tracker.html">Profit Tracker spreadsheet</a> stores
  each product's price, fees and cost and recalculates profit per product and per month — no formulas to build.
</div>
"""

write(
    "etsy-fees-2026.html",
    simple_page(
        path="etsy-fees-2026.html",
        title="Etsy Fees 2026: Every Fee Explained (with a $35 Example)",
        description="Every 2026 Etsy fee for US sellers — listing, transaction, processing, regulatory and off-site ads — with a $35 worked example showing what you really keep.",
        h1="Etsy Fees 2026: the complete breakdown",
        body_html=FEES_BODY,
    ),
)

# ======================================================================
# Etsy vs Shopify
# ======================================================================
VS_BODY = """
<p class="lede">Etsy looks expensive per sale. Shopify looks cheap per sale but charges every month whether you
sell anything or not. Here is the actual crossover point.</p>

<h2>The two fee structures</h2>
<table style="border-collapse:collapse;width:100%;max-width:720px;font-size:0.95rem">
  <tr style="border-bottom:1px solid #e5e7eb;text-align:left">
    <th style="padding:8px">Cost</th><th style="padding:8px">Etsy</th><th style="padding:8px">Shopify (Basic)</th>
  </tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Monthly platform fee</td><td style="padding:8px">$0</td><td style="padding:8px">~$39/month</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Per-sale marketplace fee</td><td style="padding:8px">6.5% transaction</td>
    <td style="padding:8px">0% on your own store</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Payment processing</td><td style="padding:8px">3% + $0.25</td>
    <td style="padding:8px">~2.9% + $0.30</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Listing fee</td><td style="padding:8px">$0.20 per listing / 4 months</td><td style="padding:8px">$0</td></tr>
  <tr style="border-bottom:1px solid #e5e7eb">
    <td style="padding:8px">Built-in buyer traffic</td><td style="padding:8px">Yes — this is what you are paying for</td><td style="padding:8px">No — you bring every visitor</td></tr>
  <tr>
    <td style="padding:8px">Ad costs</td><td style="padding:8px">Off-site ads 15%/12%; Etsy Ads optional</td>
    <td style="padding:8px">You buy ads yourself (Meta, Google, TikTok)</td></tr>
</table>

<h2>The crossover, in numbers</h2>
<p>Take a $35 item with $5.99 shipping (revenue $40.99). Assume the same 3% ad spend on both platforms and no
off-site ad attribution.</p>
<ul>
  <li><strong>Etsy:</strong> 6.5% transaction on $40.99 ($2.66) + processing $1.48 + listing $0.20 ≈ <strong>$4.34
  per sale</strong>.</li>
  <li><strong>Shopify:</strong> processing $1.49 per sale + $39/month fixed. The $39 is recovered after
  <strong>about 13 sales per month</strong>; below that, Shopify costs you more than it saves.</li>
</ul>
<p>So the question is not “which is cheaper” but <strong>“can I bring myself more than ~13 sales a month?”</strong>
If yes, Shopify’s per-sale economics win and you keep the customer relationship. If no, Etsy’s zero fixed cost is
the rational choice — and the 6.5% is the price of Etsy’s traffic.</p>

<h2>The hidden cost of leaving Etsy</h2>
<p>The fee table ignores the thing Etsy actually sells: buyers. On Shopify you pay $39/month <em>and</em> you must
generate every visitor. For a beginner, a realistic ad cost to acquire a first-time buyer is $10–$30 — often more
than Etsy’s entire fee on a $35 item.</p>
<p>The winning configuration for most small sellers is not either/or:</p>
<ul>
  <li><strong>Etsy first</strong> to learn what sells and to get reviews.</li>
  <li><strong>Shopify later</strong> for repeat buyers, bundles and custom orders, at the point where you already
  have ~20+ sales/month.</li>
</ul>

<h2>Practical decisions this changes</h2>
<ol>
  <li><strong>Under ~13 sales/month:</strong> stay on Etsy, price for the fees, do not pay for a storefront.</li>
  <li><strong>Around 20+ sales/month with repeat customers:</strong> add a store, keep Etsy as an acquisition
  channel.</li>
  <li><strong>On either platform:</strong> price from the calculator’s net-profit number, not from the listing
  price.</li>
  <li><strong>On Etsy:</strong> model the 15% off-site ad worst case — it can turn a healthy margin into a loss.</li>
</ol>
<div class="promo">
  Planning to add a store? Shopify’s own pricing and trial terms change regularly; check the current offer on
  <a href="/go/shopify">Shopify’s site</a>. (Affiliate link — see our
  <a href="/disclosure.html">disclosure</a>; it never changes the price you pay.)
</div>
<p class="small muted">Figures are 2026 estimates and vary by country, plan and payment method. Always confirm on
each platform’s pricing page.</p>
"""

write(
    "etsy-vs-shopify-fees.html",
    simple_page(
        path="etsy-vs-shopify-fees.html",
        title="Etsy vs Shopify Fees 2026: The Real Break-Even (13 Sales/Month)",
        description="Etsy vs Shopify fees in 2026, side by side, with the exact monthly sales volume where Shopify becomes cheaper — and the hidden cost of leaving Etsy's traffic.",
        h1="Etsy vs Shopify: which fees actually cost less?",
        body_html=VS_BODY,
    ),
)

# ======================================================================
# Profit Tracker (product landing page)
# ======================================================================
PRODUCT_BODY = """
<p class="lede">A spreadsheet that answers the only question that matters: which of my products actually makes
money — after every fee?</p>

<div class="tool" style="background:#fff">
  <h2>What it does</h2>
  <ul>
    <li><strong>Profit per product</strong> — enter price, shipping, marketplace fees and item cost once; the
    sheet shows net profit and margin per sale.</li>
    <li><strong>Monthly roll-up</strong> — log sales per product per month and see profit per month, per
    quarter and per year automatically.</li>
    <li><strong>Break-even price</strong> for every product, so you never price below the floor again.</li>
    <li><strong>Fee presets</strong> for Etsy, eBay, TikTok Shop and Shopify — edit a rate when a platform
    changes it.</li>
    <li><strong>Works offline.</strong> One .xlsx file, no subscription, no account, no data leaves your
    computer.</li>
  </ul>

  <h2>What's inside the file</h2>
  <ul>
    <li><code>Start here</code> — 3-step instructions, plain English</li>
    <li><code>Products</code> — one row per product, 40+ rows ready</li>
    <li><code>Monthly sales</code> — 12 months × your products, profit auto-calculated</li>
    <li><code>Fee presets</code> — the current rates, editable</li>
    <li><code>Dashboard</code> — profit per month, best product, worst product</li>
  </ul>

  <div class="promo">
    <strong>Price: $12, one time.</strong> No subscription, free updates for 12 months.
    <!-- Replace with your Gumroad / Lemon Squeezy checkout link after you turn 18 (or ask a parent to set one up). -->
    <a href="/profit-tracker.html#buy">Get the Profit Tracker</a>
  </div>

  <p class="small muted">Not a course, not a community, not a subscription. A file that does arithmetic you
  should not be doing by hand.</p>
</div>

<h2 id="buy">How to get it</h2>
<p>Checkout is handled by Gumroad (card and PayPal, instant download). The page for the file is being set up —
if the button is not live yet, <a href="/about.html">contact me</a> and I will send it directly.</p>

<h2>Who it is for</h2>
<p>Sellers doing 10–500 orders a month on one or two marketplaces who currently work out profit “roughly”. If
you have never made a sale, use the <a href="/tools/marketplace-fee-calculator.html">free calculator</a>
first — it is enough.</p>

<h2>Refund policy</h2>
<p>If the file does not open or does not calculate correctly for you, email me and I will refund it — no
questions. Digital goods, so no refunds for “changed my mind”, which is standard for downloadable files.</p>
"""

write(
    "profit-tracker.html",
    simple_page(
        path="profit-tracker.html",
        title="Marketplace Profit Tracker Spreadsheet — profit per product and per month",
        description="A ready-made Excel spreadsheet for marketplace sellers: profit per product after fees and COGS, monthly roll-up and break-even price. One-time $12 download.",
        h1="Marketplace Profit Tracker",
        body_html=PRODUCT_BODY,
    ),
)

# ======================================================================
# Legal / trust pages
# ======================================================================
write(
    "about.html",
    simple_page(
        path="about.html",
        title="About RateWise",
        description="Who runs RateWise and why the calculators are free.",
        h1="About RateWise",
        body_html="""
<p class="lede">RateWise is a small independent site with one job: show sellers the number that actually
matters — profit after fees.</p>
<p>It is run by one person, not a company. The calculators are free because the site earns a small commission
when a reader chooses to try a tool linked from an article. That is the whole business model, and it is why
there are no pop-ups, no email gate and no “sign up to see your result”.</p>
<h2>How the numbers are kept honest</h2>
<ul>
  <li>Every fee figure comes from the platform’s own pricing or seller-help pages, and is dated on the page.</li>
  <li>Every calculator lets you override the rate — platforms change fees, and your dashboard is the final
  authority.</li>
  <li>Where a page contains an affiliate link, it says so at the link and on the
  <a href="/disclosure.html">disclosure page</a>.</li>
</ul>
<h2>What this site is not</h2>
<p>It is not tax, legal or financial advice. It does arithmetic on numbers you give it. For anything that
affects your taxes or your business structure, talk to a qualified professional in your country.</p>
<h2>Contact</h2>
<p>Corrections and feature requests are welcome: <a href="mailto:hello@example.com">hello@example.com</a>
(replace with your real address before launch).</p>
""",
    ),
)

write(
    "privacy.html",
    simple_page(
        path="privacy.html",
        title="Privacy policy",
        description="What data RateWise collects and what it does not: the calculators run in your browser and your numbers are never sent to a server.",
        h1="Privacy policy",
        body_html="""
<p class="lede">Short version: the calculators run in your browser. Your numbers are never sent to a server.</p>
<h2>What we do not collect</h2>
<ul>
  <li>No account, no email required to use any calculator.</li>
  <li>No calculator input is transmitted anywhere — the maths happens in your browser.</li>
  <li>No selling of personal data, ever.</li>
</ul>
<h2>What is collected</h2>
<p>Standard web-server logs (IP address, page requested, browser type) are kept by the hosting provider for
security and debugging. If analytics or advertising is added in future, this page will say so before it goes
live, and it will use a provider that respects regional consent rules.</p>
<h2>Cookies</h2>
<p>This site sets no tracking cookies of its own. Third-party links (for example to a marketplace or a tool)
may set cookies on their own sites under their own policies.</p>
<h2>Children</h2>
<p>This site is a general-audience tool and does not knowingly collect information from anyone under 13.</p>
<h2>Questions</h2>
<p><a href="mailto:hello@example.com">hello@example.com</a></p>
""",
    ),
)

write(
    "disclosure.html",
    simple_page(
        path="disclosure.html",
        title="Affiliate disclosure",
        description="How RateWise makes money and which links are affiliate links.",
        h1="Affiliate disclosure",
        body_html="""
<p class="lede">Some links on this site are affiliate links. If you click one and buy something, the seller pays
this site a commission at no extra cost to you. That is how the calculators stay free.</p>
<h2>Which links are affiliate links</h2>
<p>Links to third-party products — for example store platforms, seller tools and software — may be affiliate
links. They are marked with a short note near the link. Links to marketplace help pages and pricing pages used
as sources are not affiliate links.</p>
<h2>What this does not change</h2>
<ul>
  <li>The price you pay is the same.</li>
  <li>Recommendations are based on the fee maths, not on which program pays more.</li>
  <li>If a tool is not worth the money for a small seller, the page says so even when an affiliate program
  exists.</li>
</ul>
<h2>Programs</h2>
<p>This site may participate in affiliate programs operated by marketplace and software companies. Program
terms and commission rates change; the maths on any page does not depend on them.</p>
<h2>Questions</h2>
<p><a href="mailto:hello@example.com">hello@example.com</a></p>
""",
    ),
)

print("done")
