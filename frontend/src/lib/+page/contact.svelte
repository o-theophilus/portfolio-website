<script>
	import { Content } from '$lib/layout';
	import Scroller from './scroller2.svelte';
	import { Observe } from '$lib/macro';
</script>

<Content --content-height="100%" --content-padding-top="80px">
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<div>
				<div class="page_title">How Can I Help?</div>
				<br />
				I am currently available for freelance work and collaborations. Whether you're looking to refresh
				your branding, create a new website, or design marketing materials, I'm here to help.
			</div>
			<div>
				<Scroller query="footer">
					get in
					<br />
					touch
				</Scroller>
			</div>
		</div>
	</Observe>
</Content>

<style>
	.observe {
		display: flex;
		gap: var(--sp2);
		align-items: center;

		max-width: 600px;

		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition:
			opacity,
			transform 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}
</style>
