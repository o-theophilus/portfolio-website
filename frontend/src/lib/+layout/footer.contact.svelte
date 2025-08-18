<script>
	import { Link } from '$lib/button';
	import { Icon } from '$lib/macro';
</script>

<div class="block">
	<Link href="tel:+2348067397793">
		<span>
			<Icon icon="phone" />
			+234 806 739 7793
		</span>
	</Link>
	<Link href="mailto:theophilus.ogbolu@gmail.com">
		<span>
			<Icon icon="mail" />
			theophilus.ogbolu&#8203;@gmail.com
		</span>
	</Link>
	<Link
		href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
		blank
	>
		<span>
			<Icon icon="map-pin" />
			Lagos, Nigeria.
		</span>
	</Link>
</div>

<style>
	.block {
		display: flex;
		flex-direction: column;
		align-items: center;

		gap: var(--sp1);
	}

	span {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
	@media screen and (min-width: 600px) {
		.block {
			align-items: unset;
		}
	}
</style>
