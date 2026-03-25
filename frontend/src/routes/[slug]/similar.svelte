<script>
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { FoldButton } from '$lib/button';
	import { Avatar, Spinner } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';

	let { similar = [], loading } = $props();
	let open = $state(true);

	const prerender = (post) => {
		app.post = post;
	};
</script>

{#if loading || similar.length}
	<div class="title line">
		<div class="page_title line">
			Similar Post{#if similar.length > 1}s{/if}
			<Spinner active={loading} size="20" />
		</div>

		{#if !loading}
			<FoldButton
				{open}
				onclick={() => {
					open = !open;
				}}
			/>
		{/if}
	</div>

	{#if open && !loading}
		<div class="post_area" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each similar as post}
				<div class="post">
					<a
						href="/{post.slug}"
						onclick={() => prerender(post)}
						onmouseenter={() => prerender(post)}
					>
						<Avatar size="58" photo={post.photo} no_photo="/no_photo.png" name={post.title}
						></Avatar>
					</a>
					<div class="details">
						<a
							class="link"
							href="/{post.slug}"
							onclick={() => {
								prerender(post);
								update(post);
							}}
							onmouseenter={() => prerender(post)}
						>
							{post.title}
						</a>

						{#if post.description}
							<br />
							<div class="desc">
								{post.description}
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{/if}
{/if}

<style>
	.title {
		justify-content: space-between;
		margin: 48px 0;
	}

	.post_area {
		display: grid;
		gap: 24px;
		margin: 48px 0;

		@media screen and (min-width: 600px) {
			& {
				grid-template-columns: 1fr 1fr;
			}
		}
	}

	.post {
		display: flex;
		gap: 16px;

		& .link {
			text-decoration: none;
			color: var(--link-color, var(--link));
			font-weight: 700;

			line-height: 10%;

			transition: color 0.2s ease-in-out;

			&:hover {
				color: var(--link-color-hover, color-mix(in srgb, var(--link), black 30%));
			}
		}

		& .desc {
			margin-top: 4px;
			font-size: 0.7rem;
		}
	}
</style>
