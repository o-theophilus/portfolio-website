<script>
	import { module, settings, user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import One from './one.svelte';
	import Edit from './mod.svelte';
	import BRound from '$lib/button/round.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
</script>

{#if $settings.highlight && $settings.highlight.length > 0}
	<Content fit>
		<div class="comp">
			<div class="title">
				<strong class="ititle">
					Some Thing{$settings.highlight.length > 1 ? 's' : ''}
					I've Built
				</strong>

				{#if $user.access.includes('post:edit_photos')}
					<BRound
						icon="edit"
						on:click={() => {
							$module = {
								module: Edit
							};
						}}
					/>
				{/if}
			</div>

			{#each $settings.highlight as post (post.key)}
				<One {post} />
			{/each}

			<Link
				href="/post"
			>
				<div class="link">
					View more
					<Icon icon="arrow_forward" />
				</div>
			</Link>
		</div>
	</Content>
{/if}

<style>
	.comp {
		margin: var(--sp5) 0;
	}

	.title {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.link {
		display: inline-flex;
		align-items: center;
		gap: var(--sp1);
		width: fit-content;
		transition: gap var(--trans);
	}

	.link:hover {
		gap: var(--sp2);
	}
</style>
