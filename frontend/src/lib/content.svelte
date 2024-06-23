<script>
	export let fit = false;
</script>

<section class:fill={!fit}>
	<slot />
</section>

<style>
	section {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	.fill {
		min-height: calc(100vh - var(--headerHeight));
	}
</style>
