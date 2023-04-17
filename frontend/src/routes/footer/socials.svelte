<script>
	import SVG from '$lib/comp/svg.svelte';
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
	<a href="https://www.linkedin.com/in/o-theophilus/" target="_blank" rel="noopener noreferrer">
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
		gap: var(--gap2);

		max-width: var(--mobileWidth);
	}
	@media screen and (min-width: 600px) {
		.block {
			justify-content: unset;
		}
	}

	a {
		--size: 20px;
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		fill: var(--accent3);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	a:hover {
		fill: var(--color1);
	}
</style>
