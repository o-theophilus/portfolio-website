<script>
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<a href="https://wa.me/2348067397793/?text=Hello%20Theophilus">
		<SVG type="whatsapp" />
	</a>
	<a href="https://m.facebook.com/o.theophilus" target="_blank" rel="noopener noreferrer">
		<SVG type="facebook" />
	</a>
	<a href="https://twitter.com/o__theophilus" target="_blank" rel="noopener noreferrer">
		<SVG type="twitter" />
	</a>
	<a
		href="https://www.linkedin.com/in/o-theophilus/"
		target="_blank"
		rel="noopener noreferrer"
	>
		<SVG type="linkedin" />
	</a>
	<a href="https://github.com/o-theophilus" target="_blank" rel="noopener noreferrer">
		<SVG type="github" />
	</a>
</div>

<style>
	.block {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;

		max-width: var(--mobileWidth);
	}
	@media screen and (min-width: 900px) {
		.block {
			justify-content: unset;
		}
	}

	a {
		display: flex;
		justify-content: center;
		align-items: center;

		width: 50px;
		height: 50px;

		border-radius: 50%;

		fill: var(--color1);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	a:hover {
		fill: var(--color3);
	}
</style>
