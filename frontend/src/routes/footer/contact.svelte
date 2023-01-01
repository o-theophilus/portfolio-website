<script>
	import SVG from '$lib/comp/svg.svelte';
</script>

<div class="block">
	<a href="tel:+2348067397793">
		<SVG type="call" size="20" />
		+234 806 739 7793
	</a>
	<a href="mailto:theophilus.ogbolu@gmail.com">
		<SVG type="email" size="20" />
		theophilus.ogbolu@gmail.com
	</a>
	<a
		href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
		target="blank"
	>
		<SVG type="location" size="20" />
		Lagos, Nigeria.
	</a>
</div>

<style>
	.block {
		display: flex;
		flex-direction: column;
		align-items: center;

		gap: var(--gap2);
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

		color: var(--font);
		text-decoration: none;
		fill: var(--font);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a:hover {
		color: var(--color1);
		fill: var(--color1);
	}
</style>
