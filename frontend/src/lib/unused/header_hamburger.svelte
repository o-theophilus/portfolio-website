<script>
	import Humburger from './humburger.svelte';
</script>

<div class="topBar">
	<div class="block">
		<Humburger />
	</div>
</div>

<style>
	.topBar {
		position: fixed;
		top: 0;
		z-index: 3;
		height: var(--headerHeight);

		width: 100%;
		pointer-events: none;
	}
	@media screen and (min-width: 900px) {
		.topBar {
			display: none;
		}
	}

	.block {
		position: relative;
		max-width: var(--mobileWidth2);
		height: 100%;

		margin: auto;
	}
</style>
