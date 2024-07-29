<script>
	export let password = '';
</script>

<div class="block main">
	<div class="block">
		<div class="one" class:active={password && /[a-z]/.test(password)}>
			lowercase{#if password && /[a-z]/.test(password)}&nbsp;&#10003;{/if}
		</div>
		<div class="one" class:active={password && /[A-Z]/.test(password)}>
			uppercase{#if password && /[A-Z]/.test(password)}&nbsp;&#10003;{/if}
		</div>
	</div>

	<div class="block">
		<div class="one" class:active={password && /[0-9]/.test(password)}>
			number{#if password && /[0-9]/.test(password)}&nbsp;&#10003;{/if}
		</div>
		<div class="one" class:active={password && password.length >= 8 && password.length <= 18}>
			8 - 18 length{#if password && password.length >= 8 && password.length <= 18}&nbsp;&#10003;{/if}
		</div>
	</div>
</div>

<style>
	.block {
		display: flex;
		gap: 2px;
		width: 100%;
	}

	.block .block {
		flex-wrap: wrap;
	}

	@media screen and (min-width: 380px) {
		.block .block {
			flex-wrap: nowrap;
		}
	}

	.main {
		margin-top: 4px;
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
		background-color: var(--bg2);
		transition: background-color var(--trans), color var(--trans);

		width: 100%;
	}

	.active {
		color: var(--ft1_b);
		background-color: var(--cl3);
	}
</style>
