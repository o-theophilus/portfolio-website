<script>
	import Content from '$lib/content.svelte';
	import Scroller from '$lib/scroller.svelte';
	import Observe from '$lib/observe.svelte';
</script>

<div class="scroll_1" />
<br /><br />
<Content>
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="big dark"> Hi. </strong>
			<br /><br />
			I am a web developer/graphic designer based in Lagos. I have a passion for designing, and I love
			to create for the web and mobile devices.
		</div>
	</Observe>

	<br /><br />

	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="big color1"> What I can do. </strong>
			<br /><br />
			<strong class="large">Design what you want.</strong>
			<br />
			<br />
			I like to keep it simple. My goals are focused on details, content and conveying the message that
			you want to send.
		</div>
	</Observe>

	<br /><br />

	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="large">Develop what you need.</strong>
			<br />
			<br />
			I am a developer, so I know how to create your website to run across devices using the latest technologies
			available.
		</div>
	</Observe>

	<br /><br />

	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<div class="h">
				<div>
					<strong class="big color1"> I can help. </strong>
					<br /><br />
					I am currently available for freelance work. If you have a project that you want to get started,
					think you need my help with something or just fancy saying hey...
					<!--, then get in touch.-->
				</div>
				<div>
					<Scroller query="footer">
						get in
						<br />
						touch
					</Scroller>
				</div>
			</div>
		</div>
	</Observe>
</Content>

<style>
	.h {
		display: flex;
		gap: var(--gap2);
		align-items: center;
	}

	.observe {
		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition: opacity, transform 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}

	.dark {
		color: var(--accent1);
	}
	.large {
		color: var(--accent1);
		font-size: large;
	}
</style>
