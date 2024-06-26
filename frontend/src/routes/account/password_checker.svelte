<script>
	export let password = '';
</script>

<section>
	<div class:active={password && /[a-z]/.test(password)}>lowercase</div>
	|
	<div class:active={password && /[A-Z]/.test(password)}>uppercase</div>
	|
	<div class:active={password && /[0-9]/.test(password)}>number</div>
	|
	<div class:active={password && password.length >= 8 && password.length <= 18}>8 - 18 length</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp0);

		border-radius: var(--brad1);
		overflow: hidden;

		font-size: small;
		color: var(--overlay);
	}
	.active {
		color: var(--cl3);
	}

	div {
		flex-shrink: 0;
	}
</style>
