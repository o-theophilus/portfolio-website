<script>
	let { children } = $props();
</script>

<section>
	{@render children()}
</section>

<style>
	section {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 24px;
		padding-top: var(--content-padding-top, 24px);
		padding-bottom: var(--content-padding-bottom, 24px);
		min-height: var(--content-height, calc(100vh - var(--headerHeight)));
	}
</style>
