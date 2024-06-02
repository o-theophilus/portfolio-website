<script>
	export let password = '';
</script>

<section>
	<div class:active={password && /[a-z]/.test(password)}>lowercase</div>
	<div class:active={password && /[A-Z]/.test(password)}>uppercase</div>
	<div class:active={password && /[0-9]/.test(password)}>number</div>
	<div class:active={password && password.length >= 8 && password.length <= 18}>
		8 - 18 characters
	</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp1);

		border-radius: var(--brad1);
		overflow: hidden;

		font-size: x-small;
		color: var(--ac4);
	}
	.active {
		color: var(--cl3);
	}
</style>
