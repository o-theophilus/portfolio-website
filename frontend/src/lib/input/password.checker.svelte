<script>
	let { value } = $props();
</script>

<div class="main">
	<div class="block">
		<div class="one" class:active={value && /[a-z]/.test(value)}>
			lowercase{#if value && /[a-z]/.test(value)}&nbsp;&#10003;{/if}
		</div>
		<div class="one" class:active={value && /[A-Z]/.test(value)}>
			uppercase{#if value && /[A-Z]/.test(value)}&nbsp;&#10003;{/if}
		</div>
	</div>

	<div class="block">
		<div class="one" class:active={value && /[0-9]/.test(value)}>
			number{#if value && /[0-9]/.test(value)}&nbsp;&#10003;{/if}
		</div>
		<div class="one" class:active={value && value.length >= 8 && value.length <= 18}>
			8 - 18 length{#if value && value.length >= 8 && value.length <= 18}&nbsp;&#10003;{/if}
		</div>
	</div>
</div>

<style>
	.main,
	.block {
		display: flex;
		gap: 2px;
		width: 100%;
	}

	.block {
		flex-wrap: wrap;
	}

	@media screen and (min-width: 380px) {
		.block {
			flex-wrap: nowrap;
		}
	}

	.one {
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;

		padding: 4px;
		border-radius: 4px;

		font-size: 0.6rem;
		color: var(--ft2);
		background-color: var(--bg1);
		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;

		width: 100%;
	}

	.active {
		color: white;
		background-color: green;
	}
</style>
