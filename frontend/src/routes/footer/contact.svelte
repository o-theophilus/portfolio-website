<script>
	import Button from '$lib/comp/button.svelte';
</script>

<div class="block">
	<Button icon="call" class="secondary" href="tel:+2348067397793">+234 806 739 7793</Button>
	<Button icon="email" class="secondary" href="mailto:theophilus.ogbolu@gmail.com">
		theophilus.ogbolu@gmail.com
	</Button>
	<Button
		icon="location"
		class="secondary"
		href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
		target="blank"
	>
		Lagos, Nigeria.
	</Button>
</div>

<style>
	.block {
		display: flex;
		flex-direction: column;
		align-items: center;

		gap: var(--gap1);
	}
	@media screen and (min-width: 500px) {
		.block {
			align-items: unset;
		}
	}
</style>
