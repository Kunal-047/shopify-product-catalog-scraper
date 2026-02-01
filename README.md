# Shopify Product Catalog Scraper → Shopify Import CSV

## Overview

This project scrapes Amazon product pages (or category pages) and converts them into a **Shopify-import-ready CSV**.

The primary goal is **zero manual cleanup**: the generated CSV uploads directly into Shopify using the native product import feature, without errors or post-processing.

This is **not a generic web scraper**. All scraping and transformation logic is designed specifically around Shopify’s product import schema and constraints.

---

## Input

* A list of Amazon product URLs

  * Individual product pages
  * (Optionally) category or search result pages

URLs are provided externally and are not hardcoded.

---

## Output

* A clean, duplicate-free **Shopify-compatible CSV**

Each product in the CSV includes:

### Core Product Fields

* **Handle**

  * Auto-generated from product title
  * Lowercase, hyphenated, URL-safe
  * Shared across all variants of the same product

* **Title**

  * Clean product title

* **Body (HTML)**

  * Sanitized product description
  * No scripts, ads, tracking elements, or junk text

* **Vendor**

  * Extracted brand or manufacturer (e.g., Apple, Samsung, Nike)
  * Marketplace or storefront names are explicitly excluded
  * Normalized for consistency across products

* **Product Type / Category**

  * Derived from product metadata where available

---

## Images

* Product image URLs are extracted and mapped to Shopify image fields
* Only valid, Shopify-compatible image URLs are included
* Duplicate images are removed

---

## Variants

When applicable, product variants are fully supported.

### Variant Handling Logic

* Variant attributes such as:

  * Size
  * Color
  * Storage
  * Capacity
  * Other selectable options

* Each variant:

  * Appears as a **separate row** in the CSV
  * Shares the same **Handle** as its parent product
  * Has a **unique SKU**

### SKU Generation

* If the source page provides SKUs, they are used
* If SKUs are missing:

  * Deterministic, readable SKUs are generated based on:

    * Product handle
    * Variant attributes

---

## Data Integrity & De-duplication

* Duplicate products are removed
* Duplicate variants are removed
* Variant grouping is validated to ensure correct parent-child relationships

---

## Shopify Compatibility

* CSV strictly follows Shopify’s official product import format
* Column names, ordering, and data types are Shopify-safe
* Tested with direct CSV upload into Shopify Admin

**Result:** The CSV imports successfully without warnings or errors.

---

## Project Scope

Included:

* Scraping logic
* Data normalization and cleanup
* Shopify CSV formatting

Not included:

* Storefront or UI
* Hosting or deployment
* Shopify API integration

CSV output only.

---

## Deliverables

* Final Shopify-ready CSV
* Scraper and transformation logic
* Clear, documented rules for:

  * Handle generation
  * Vendor normalization
  * Variant grouping
  * SKU generation

---

## Notes

* Designed for reliability and repeatability
* Safe for bulk product imports
* Easily extendable for other marketplaces or schemas

