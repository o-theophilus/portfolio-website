<script>
	import Observe from '$lib/observe.svelte';
	import Content from '$lib/content.svelte';
</script>

<div id="about" />
<Content>
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="big">About Me</strong>
			<br /><br />

			My name is <strong>Theophilus</strong>, and I am a self-taught programmer and designer with a
			passion for learning and growing. I am always seeking new challenges and opportunities to
			expand my skills and knowledge.

			<br /> <br />
			I spend most of my time working on personal projects, contributing to open source projects, and
			sharing my knowledge with others. I believe in the power of community and collaboration and have
			benefited greatly from the support and mentorship of others.
			<br /> <br />

			When I am not designing or programming, you can find me playing music, exploring my
			surroundings, or spending time with my family and friends. I believe that a balanced and
			fulfilling life is essential to creative inspiration and success.
		</div>
	</Observe>
</Content>

<style>
	.observe {
		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition: all 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}

	.big {
		color: var(--ac1);
	}
</style>
