<script>
	import Content from '$lib/content.svelte';
	import Scroller from '$lib/scroller.svelte';
	import Observe from '$lib/observe.svelte';
</script>

<Content fit>
	<div class="scroll_2">
		<Observe let:intersecting>
			<div class="observe" class:intersecting>
				<div>
					<strong class="ititle"> How Can I Help? </strong>
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
	</div>
</Content>

<style>
	.scroll_2 {
		margin: var(--sp5) 0;
	}

	.observe {
		display: flex;
		gap: var(--sp2);
		align-items: center;

		max-width: 600px;

		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition: opacity, transform 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}
</style>
