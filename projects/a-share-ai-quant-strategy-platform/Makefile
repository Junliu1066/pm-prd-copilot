.PHONY: check-docs check-compliance check-contracts check-prototype check-boundary check-all

check-docs:
	@bash scripts/check-docs.sh

check-compliance:
	@bash scripts/check-compliance.sh

check-contracts:
	@bash scripts/check-contracts.sh

check-prototype:
	@bash scripts/check-prototype.sh

check-boundary:
	@bash scripts/check-thread-boundary.sh

check-all: check-docs check-compliance check-contracts check-prototype check-boundary
