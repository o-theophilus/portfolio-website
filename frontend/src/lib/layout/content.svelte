<script>
	let { fit = false, children } = $props();
</script>

<section class:fill={!fit}>
	{@render children()}
</section>

<style>
	section {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp3);
	}

	.fill {
		min-height: calc(100vh - var(--headerHeight));
	}
</style>
