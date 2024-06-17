<script>
</script>

<section>
	<slot />
</section>

<style>
	section {
		max-width: var(--mobileWidth);
		width: 100%;
		min-height: calc(100vh - var(--headerHeight));
		margin: auto;
		padding: 0 var(--sp2);
	}
</style>
