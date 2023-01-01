<script>
</script>

<section class="content_no_margin">
	<slot />
</section>

<style>
	section {
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--gap4);

		color: var(--font);
	}

	/* :global(.content_no_margin) * {
		margin: 0;
		padding: 0;
	} */
</style>
