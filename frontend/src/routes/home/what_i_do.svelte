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
			<strong class="ititle dark"> Hi There! </strong>
			<br />
			I am a multidisciplinary designer with a passion for creating impactful designs for web and print.
			From logos to brochures, websites to social media graphics, I've got you covered.
		</div>
	</Observe>

	<br /><br />

	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="ititle color"> What I Can Do: </strong>
			<br /><br />
			<strong>Design What You Want</strong>
			<br />
			My design philosophy centers on simplicity and clarity. I believe in creating designs that are
			not only aesthetically pleasing, but also easy to understand and effective in communicating your
			message.
		</div>
	</Observe>

	<br />

	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong>Develop What You Need</strong>
			<br />
			While I focus primarily on graphic design, I also have experience with web development and programming.
			I can work with you to create a website that not only looks great, but also functions seamlessly
			across devices.
		</div>
	</Observe>

	<br /><br />

	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<div class="h">
				<div>
					<strong class="ititle color"> How I Can Help </strong>
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
		</div>
	</Observe>
</Content>

<style>
	.h {
		display: flex;
		gap: var(--sp2);
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
		color: var(--ft1);
	}
	.color {
		color: var(--cl1);
	}
</style>
