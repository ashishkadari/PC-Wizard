# PC Wizard

-Welcome! This project is a full-stack application I built during sixth form. PC Wizard is a build generator that scrapes live retailer data, enforces compatibility constraints, and assembles optimised gaming/workstation configurations within budget. The recommendation engine is powered by recursive backtracking, ensuring every build is both valid and cost-efficient.

# Key Features

Recursive build generation: Backtracking algorithm explores possible component combinations, pruning incompatible or over-budget paths in real time.

Compatibility enforcement: Validates CPU–motherboard socket matching, RAM type alignment (DDR4 vs DDR5), and PSU power requirements during the build process.

Web scraping pipeline: Collects live product data (names, specs, prices, links) from a UK retailer using Requests/Selenium + XPath, with pagination handling and fallback scraping.

Database integration: Stores and queries structured component data in SQLite, enabling efficient lookups and incremental build assembly.

Adaptive search order: Build logic changes depending on target use case (gaming vs workstation), prioritising GPUs or CPUs for more efficient recursion.

Extensibility: New components or constraints (e.g. cooling, case size) can be added to the recursive search with minimal changes.
