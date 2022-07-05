<script>
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<a href="tel:+2348067397793">
		<SVG type="call" size="20" />
		<p>+234 806 739 7793</p>
	</a>
	<a href="mailto:theophilus.ogbolu@gmail.com">
		<SVG type="email" size="20" />
		<p>theophilus.ogbolu@gmail.com</p>
	</a>
	<a
		href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
		target="blank"
	>
		<SVG type="location" size="20" />
		<p>Lagos, Nigeria.</p>
	</a>
</div>

<style>
	* {
		padding: 0;
		margin: 0;
	}
	.block {
		display: flex;
		flex-direction: column;
		align-items: center;

		max-width: var(--mobileWidth);

		color: var(--color1);
		gap: 10px;
	}
	@media screen and (min-width: 900px) {
		.block {
			align-items: unset;
		}
	}
	a {
		display: flex;
		gap: 20px;
		align-items: center;

		color: var(--fColor1);
		text-decoration: none;
		fill: var(--color1);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a:hover {
		color: var(--color3);
		fill: var(--color3);
	}
</style>
