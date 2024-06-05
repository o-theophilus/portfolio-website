<script>
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<a href="https://wa.me/2348067397793/?text=Hello%20Theophilus">
		<SVG type="whatsapp" />
	</a>
	<a href="https://twitter.com/o__theophilus" target="_blank" rel="noopener noreferrer">
		<SVG type="twitter" />
	</a>
	<a href="https://github.com/o-theophilus" target="_blank" rel="noopener noreferrer">
		<SVG type="github" />
	</a>
	<!-- <a href="https://discord.com/users/theophilus#6682" target="_blank" rel="noopener noreferrer">
		<SVG type="discord" />
	</a> -->
	<a href="https://m.facebook.com/o.theophilus" target="_blank" rel="noopener noreferrer">
		<SVG type="facebook" />
	</a>
	<!-- <a href="https://www.instagram.com/o_theophilus_/" target="_blank" rel="noopener noreferrer">
		<SVG type="instagram" />
	</a> -->
	<a href="https://www.linkedin.com/in/o-theophilus/" target="_blank" rel="noopener noreferrer">
		<SVG type="linkedin" />
	</a>
</div>

<style>
	.block {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--sp2);

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

		fill: var(--ac3);

		transition: fill var(--trans);
	}

	a:hover {
		fill: var(--cl1);
	}
</style>
