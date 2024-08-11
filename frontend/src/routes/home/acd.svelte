<script>
	import { onMount } from 'svelte';

	import Content from '$lib/content.svelte';
	import Icon from '$lib/icon.svelte';
	import Observe from '$lib/observe.svelte';

	onMount(() => {
		let op = {
			threshold: 0,
			rootMargin: '-20% 0px'
		};
		let cb = (elements, ob) => {
			for (const elem of elements) {
				if (elem.isIntersecting) {
					elem.target.classList.add('intersecting');
					ob.unobserve(elem.target);
				}
			}
		};

		let ob = new IntersectionObserver(cb, op);

		ob.observe(document.querySelector('.card:nth-of-type(1)'));
		ob.observe(document.querySelector('.card:nth-of-type(2)'));
		ob.observe(document.querySelector('.card:nth-of-type(3)'));
	});
</script>

<div class="intersecting" style="display: none;">
	<div class=" pos" />
</div>

<Content fit>
	<div class="comp">
		<Observe let:intersecting>
			<div class="observe">
				<strong class="ititle"> What I Can Do </strong>
			</div>
		</Observe>

		<div class="block">
			<div class="card">
				<div class="pos">
					<div class="icon one">
						<Icon icon="design" size="1.5" />
					</div>
					<div class="title">Design What You Want</div>

					<div class="text">
						My design philosophy centers on simplicity and clarity. I believe in creating designs
						that are not only aesthetically pleasing, but also easy to understand and effective in
						communicating your message.
					</div>
				</div>
			</div>

			<div class="card">
				<div class="pos">
					<div class="icon two">
						<Icon icon="code2" size="1.5" />
					</div>
					<div class="title">Develop What You Need</div>

					<div class="text">
						While I focus primarily on graphic design, I also have experience with web development
						and programming. I can work with you to create a website that not only looks great, but
						also functions seamlessly across devices.
					</div>
				</div>
			</div>

			<div class="card">
				<div class="pos">
					<div class="icon three">
						<Icon icon="brush" size="1.5" />
					</div>
					<div class="title">Create What Inspires</div>

					<div class="text">
						My approach to art focuses on clear expression and effective communication. I strive to
						create artworks that are visually engaging and evoke strong emotions. My goal is to
						produce pieces that are not only appealing but also meaningful and thought-provoking.
					</div>
				</div>
			</div>
		</div>
	</div>
</Content>

<style>
	.comp {
		margin: var(--sp5) 0;
	}

	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);
		margin: var(--sp2) 0;
	}

	@media screen and (min-width: 600px) {
		.block {
			flex-direction: unset;
		}
	}

	.card {
		width: 100%;
	}
	.card:nth-of-type(1) {
		--color: var(--cl6);
	}
	.card:nth-of-type(2) {
		--color: var(--cl3);
	}
	.card:nth-of-type(3) {
		--color: var(--cl5);
	}

	.pos {
		--trans1: 0.5s cubic-bezier(0.47, 1.64, 0.41, 0.8);

		/* padding: var(--sp2); */
		border-radius: var(--sp0);
		/* background-color: color-mix(in srgb, var(--color), transparent 90%); */

		height: 100%;

		opacity: 0;
		transform: translateY(400px) scale(0);
		transition: transform var(--trans1), opacity var(--trans);
	}

	.intersecting .pos {
		transform: translateY(0);
		opacity: 1;
	}

	@media screen and (min-width: 600px) {
		.card:nth-of-type(2) .pos {
			transition: transform var(--trans1) 0.5s, opacity var(--trans1) 0.5s;
		}
		.card:nth-of-type(3) .pos {
			transition: transform var(--trans1) 1s, opacity var(--trans1) 1s;
		}
	}

	.icon {
		--size: 48px;

		display: flex;
		justify-content: center;
		align-items: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);

		color: var(--color);

		color: var(--clb);
		background-color: var(--color);
	}

	.title {
		margin: var(--sp1) 0;

		font-weight: 800;
		font-size: 1.1rem;
		color: var(--color);
	}
</style>
