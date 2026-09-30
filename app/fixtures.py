# Paypage Ledger — local HTML fixtures (no network required for health tests)
# Signature: Mourad.Soltani

CHECKOUT_HTML_V1 = """
<!doctype html>
<html>
  <head>
    <script src="https://js.stripe.com/v3/"></script>
    <script src="https://pay.example.com/checkout.js"></script>
  </head>
  <body>
    <form id="pay"></form>
    <script>
      window.PAYPAGE = { merchant: "demo" };
    </script>
  </body>
</html>
"""

CHECKOUT_HTML_V2 = """
<!doctype html>
<html>
  <head>
    <script src="https://js.stripe.com/v3/"></script>
    <script src="https://cdn.unknown.example/inject.js"></script>
  </head>
  <body>
    <form id="pay"></form>
    <script>
      window.PAYPAGE = { merchant: "demo", extra: true };
    </script>
  </body>
</html>
"""

FIXTURES = {
    "fixture://checkout": CHECKOUT_HTML_V1,
    "fixture://checkout-changed": CHECKOUT_HTML_V2,
}
