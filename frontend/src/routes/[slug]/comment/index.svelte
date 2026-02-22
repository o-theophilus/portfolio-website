<script>
	import { app, module } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { Login } from '$lib/auth';
	import { Button, FoldButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown } from '$lib/input';
	import { Icon, Spinner } from '$lib/macro';
	import Add from './_add.svelte';
	import One from './one.svelte';

	let { post, comment, loading } = $props();

	let comments = $derived(comment.comments);
	let order_by = $derived(comment.order_by);

	let open = $derived(comments?.length > 0);
	let search = $state({
		order: 'oldest',
		page_no: 1
	});

	const update = (data) => {
		comments = data;
	};

	export const load = async () => {
		loading = true;

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/${post.key}/comments?${new URLSearchParams(search).toString()}`,
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		resp = await resp.json();

		if (resp.status == 200) {
			comments = resp.comments;
		}

		loading = false;
	};
</script>

<hr />

<div class="line space">
	<div class="line">
		<span class="page_title">
			{#if comments?.length > 0}
				{comments?.length}
			{/if}
			Comment{#if comments?.length > 1}s{/if}
		</span>
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
	<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if comments?.length > 1}
			<Dropdown
				--select-height="10"
				--select-padding-x="0"
				--select-font-size="0.8rem"
				--select-background-color="transparent"
				--select-background-color-hover="transparent"
				--select-color-hover="var(--ft1)"
				--select-outline-color="transparent"
				list={order_by}
				icon="arrow-down-narrow-wide"
				icon2="chevron-down"
				bind:value={search.order}
				onchange={(v) => {
					search.page_no = 1;
					load();
				}}
			/>
		{/if}

		{#each comments as comment (comment.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<One {comment} {post} {search} {update}></One>
			</div>
		{:else}
			<PageNote>
				<Icon icon="message-circle-off" size="50" />
				No comment
			</PageNote>
		{/each}
	</div>
{/if}

<div class="button">
	{#if app.login}
		<Button icon="message-circle-plus" onclick={() => module.open(Add, { post, update, search })}>
			Add comment
		</Button>
	{:else}
		<Button icon="log-in" onclick={() => module.open(Login)}>Login to add comment</Button>
	{/if}
</div>

<style>
	.button {
		margin: 16px 0;
	}

	hr {
		margin: 16px 0;
	}
</style>
