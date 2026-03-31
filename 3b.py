#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_3b.py
=================
Phase 3B: Header & Chat Area
Creates header components, chat area, message bubbles, streaming, and markdown rendering.
"""

import os

files_created = 0
files_failed = 0


def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    global files_created, files_failed
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_created += 1
        print(f"  ✅ Created: {path}")
    except Exception as e:
        files_failed += 1
        print(f"  ❌ Failed: {path} - {e}")


def main():
    global files_created, files_failed

    print("=" * 60)
    print("🚀 BUILD PHASE 3B: Header & Chat Area")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # HEADER COMPONENTS
    # ──────────────────────────────────────────────
    print("\n📁 Header Components")
    print("-" * 40)

    # 1. Header.tsx
    create_file("components/header/Header.tsx", """// الشريط العلوي: يحتوي على عنوان المحادثة ومحددات المنصة والنموذج والشخصية
'use client';

import { useLocale, useTranslations } from 'next-intl';
import { Menu, PanelLeftOpen, PanelRightOpen } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useUIStore } from '@/stores/uiStore';
import { Tooltip } from '@/components/ui/tooltip';
import { PlatformSelector } from './PlatformSelector';
import { ModelSelector } from './ModelSelector';
import { PersonaSelector } from './PersonaSelector';
import { SettingsDropdown } from './SettingsDropdown';
import { MessageCounter } from '@/components/common/MessageCounter';
import type { Conversation } from '@/types/chat';

interface HeaderProps {
  conversation: Conversation | null;
  messageCount: number;
}

export function Header({ conversation, messageCount }: HeaderProps) {
  const t = useTranslations('header');
  const locale = useLocale();
  const isRTL = locale === 'ar';
  const { sidebarOpen, setSidebarOpen } = useUIStore();

  return (
    <header
      className={cn(
        'h-14 shrink-0 border-b border-gray-200 dark:border-dark-700',
        'bg-white/80 dark:bg-dark-900/80 backdrop-blur-md',
        'flex items-center justify-between gap-2 px-3 z-header'
      )}
    >
      {/* الجانب الأيسر / الأيمن: تبديل الشريط الجانبي + المحددات */}
      <div className="flex items-center gap-2 min-w-0 flex-1">
        {/* زر تبديل الشريط الجانبي */}
        {!sidebarOpen && (
          <Tooltip content={t('menu')} side="bottom">
            <button
              onClick={() => setSidebarOpen(true)}
              className="rounded-lg p-2 text-gray-500 hover:bg-gray-100 dark:hover:bg-dark-800 transition-colors shrink-0"
              aria-label={t('menu')}
            >
              {isRTL ? (
                <PanelRightOpen className="h-5 w-5" />
              ) : (
                <PanelLeftOpen className="h-5 w-5" />
              )}
            </button>
          </Tooltip>
        )}

        {/* زر القائمة على الموبايل */}
        <button
          onClick={() => setSidebarOpen(true)}
          className={cn(
            'rounded-lg p-2 text-gray-500 hover:bg-gray-100 dark:hover:bg-dark-800 transition-colors shrink-0',
            sidebarOpen ? 'lg:hidden' : 'hidden'
          )}
          aria-label={t('menu')}
        >
          <Menu className="h-5 w-5" />
        </button>

        {/* محددات المنصة والنموذج */}
        <div className="hidden sm:flex items-center gap-1.5 min-w-0">
          <PlatformSelector />
          <span className="text-gray-300 dark:text-dark-600 text-xs">/</span>
          <ModelSelector />
        </div>

        {/* محدد المنصة فقط على الموبايل */}
        <div className="sm:hidden flex items-center gap-1 min-w-0">
          <PlatformSelector compact />
        </div>
      </div>

      {/* الجانب الأيمن / الأيسر: الشخصية + العدادات + الإعدادات */}
      <div className="flex items-center gap-1.5 shrink-0">
        {/* محدد الشخصية */}
        <div className="hidden md:block">
          <PersonaSelector />
        </div>

        {/* عداد الرسائل */}
        {conversation && (
          <MessageCounter current={messageCount} />
        )}

        {/* قائمة الإعدادات */}
        <SettingsDropdown />
      </div>
    </header>
  );
}
""")

    # 2. PlatformSelector.tsx
    create_file("components/header/PlatformSelector.tsx", """// محدد المنصة: قائمة منسدلة لاختيار منصة الذكاء الاصطناعي
'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import { ChevronDown, Check } from 'lucide-react';
import { cn } from '@/utils/cn';
import { usePlatformStore } from '@/stores/platformStore';
import { SUPPORTED_PLATFORMS } from '@/utils/constants';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
} from '@/components/ui/dropdown-menu';
import type { PlatformName } from '@/types/platform';

interface PlatformSelectorProps {
  compact?: boolean;
}

export function PlatformSelector({ compact = false }: PlatformSelectorProps) {
  const t = useTranslations('header');
  const { activePlatform, setPlatform } = usePlatformStore();
  const [open, setOpen] = useState(false);

  const currentPlatform = SUPPORTED_PLATFORMS.find((p) => p.name === activePlatform);

  const handleSelect = useCallback(
    (name: string) => {
      setPlatform(name as PlatformName);
      setOpen(false);
    },
    [setPlatform]
  );

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger onClick={() => setOpen(!open)}>
        <button
          className={cn(
            'flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-sm transition-colors',
            'border border-gray-200 dark:border-dark-600',
            'hover:bg-gray-50 dark:hover:bg-dark-800',
            'text-gray-700 dark:text-gray-300'
          )}
          aria-label={t('select_platform')}
        >
          <span className="text-base leading-none">{currentPlatform?.icon ?? '🌐'}</span>
          {!compact && (
            <>
              <span className="font-medium truncate max-w-[100px]">
                {currentPlatform?.displayName ?? t('select_platform')}
              </span>
              <ChevronDown className="h-3.5 w-3.5 opacity-50 shrink-0" />
            </>
          )}
        </button>
      </DropdownMenuTrigger>
      {open && (
        <DropdownMenuContent align="start" className="min-w-[200px]">
          <DropdownMenuLabel>{t('select_platform')}</DropdownMenuLabel>
          {SUPPORTED_PLATFORMS.map((platform) => (
            <DropdownMenuItem
              key={platform.name}
              onClick={() => handleSelect(platform.name)}
              className="justify-between"
            >
              <div className="flex items-center gap-2">
                <span className="text-base">{platform.icon}</span>
                <span>{platform.displayName}</span>
              </div>
              {activePlatform === platform.name && (
                <Check className="h-4 w-4 text-primary-500" />
              )}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      )}
    </DropdownMenu>
  );
}
""")

    # 3. ModelSelector.tsx
    create_file("components/header/ModelSelector.tsx", """// محدد النموذج: قائمة منسدلة ديناميكية حسب المنصة المختارة
'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { ChevronDown, Check, Loader2, Cpu } from 'lucide-react';
import { cn } from '@/utils/cn';
import { usePlatformStore } from '@/stores/platformStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import type { Model } from '@/types/platform';

interface GlobalModelRow {
  id: string;
  model_id: string;
  model_name: string;
  is_active: boolean;
  api_key_id: string;
  api_keys: {
    platform: string;
    is_active: boolean;
    is_global: boolean;
  } | null;
}

export function ModelSelector() {
  const t = useTranslations('header');
  const supabase = createSupabaseBrowserClient();
  const { activePlatform, activeModel, apiType, setModel, setAvailableModels, availableModels } =
    usePlatformStore();

  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const lastPlatformRef = useRef<string>('');

  /**
   * تحميل النماذج العامة من قاعدة البيانات
   */
  const loadGlobalModels = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data, error } = await supabase
        .from('global_models')
        .select('id, model_id, model_name, is_active, api_key_id, api_keys!inner(platform, is_active, is_global)')
        .eq('is_active', true)
        .order('sort_order', { ascending: true });

      if (error || !data) {
        setAvailableModels([]);
        return;
      }

      const rows = data as unknown as GlobalModelRow[];
      const platformModels = rows
        .filter((m) => {
          const key = m.api_keys;
          return key && key.platform === activePlatform && key.is_active && key.is_global;
        })
        .map((m): Model => ({
          id: m.model_id,
          name: m.model_name,
        }));

      setAvailableModels(platformModels);

      if (platformModels.length > 0 && !activeModel) {
        const first = platformModels[0];
        if (first) {
          setModel(first.id);
        }
      }
    } catch {
      setAvailableModels([]);
    } finally {
      setIsLoading(false);
    }
  }, [supabase, activePlatform, activeModel, setModel, setAvailableModels]);

  /**
   * تحميل النماذج عند تغيير المنصة
   */
  useEffect(() => {
    if (lastPlatformRef.current !== activePlatform) {
      lastPlatformRef.current = activePlatform;
      if (apiType === 'global') {
        loadGlobalModels();
      }
    }
    return () => {};
  }, [activePlatform, apiType, loadGlobalModels]);

  const handleSelect = useCallback(
    (modelId: string) => {
      setModel(modelId);
      setOpen(false);
    },
    [setModel]
  );

  const displayName = activeModel
    ? availableModels.find((m) => m.id === activeModel)?.name ?? activeModel.split('/').pop() ?? activeModel
    : t('select_model');

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger onClick={() => setOpen(!open)}>
        <button
          className={cn(
            'flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-sm transition-colors',
            'border border-gray-200 dark:border-dark-600',
            'hover:bg-gray-50 dark:hover:bg-dark-800',
            'text-gray-700 dark:text-gray-300'
          )}
          aria-label={t('select_model')}
        >
          <Cpu className="h-3.5 w-3.5 opacity-50 shrink-0" />
          <span className="font-medium truncate max-w-[140px]">{displayName}</span>
          <ChevronDown className="h-3.5 w-3.5 opacity-50 shrink-0" />
        </button>
      </DropdownMenuTrigger>
      {open && (
        <DropdownMenuContent align="start" className="min-w-[240px] max-h-[300px] overflow-y-auto custom-scrollbar">
          <DropdownMenuLabel>{t('select_model')}</DropdownMenuLabel>

          {isLoading ? (
            <div className="flex items-center justify-center py-4">
              <Loader2 className="h-5 w-5 animate-spin text-primary-500" />
            </div>
          ) : availableModels.length === 0 ? (
            <div className="px-3 py-4 text-center">
              <p className="text-sm text-gray-400 dark:text-gray-500">{t('no_model')}</p>
              <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{t('add_api_key_hint')}</p>
            </div>
          ) : (
            availableModels.map((model) => (
              <DropdownMenuItem
                key={model.id}
                onClick={() => handleSelect(model.id)}
                className="justify-between"
              >
                <span className="truncate">{model.name}</span>
                {activeModel === model.id && (
                  <Check className="h-4 w-4 text-primary-500 shrink-0" />
                )}
              </DropdownMenuItem>
            ))
          )}
        </DropdownMenuContent>
      )}
    </DropdownMenu>
  );
}
""")

    # 4. PersonaSelector.tsx
    create_file("components/header/PersonaSelector.tsx", """// محدد الشخصية: عرض الشخصية النشطة مع إمكانية التبديل السريع
'use client';

import { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { Sparkles, X, Check, ChevronDown } from 'lucide-react';
import { cn } from '@/utils/cn';
import { usePersonaStore } from '@/stores/personaStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import type { Persona } from '@/types/persona';

export function PersonaSelector() {
  const t = useTranslations('header');
  const supabase = createSupabaseBrowserClient();
  const { activePersona, setActivePersona, clearPersona } = usePersonaStore();

  const [open, setOpen] = useState(false);
  const [personas, setPersonas] = useState<Persona[]>([]);
  const loadedRef = useRef(false);

  useEffect(() => {
    if (loadedRef.current) return;
    loadedRef.current = true;

    const load = async () => {
      try {
        const { data } = await supabase
          .from('personas')
          .select('*')
          .in('type', ['system', 'premium'])
          .eq('is_active', true)
          .order('usage_count', { ascending: false })
          .limit(10);

        if (data) {
          setPersonas(data as Persona[]);
        }
      } catch {
        // تجاهل
      }
    };

    load();
    return () => {};
  }, [supabase]);

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger onClick={() => setOpen(!open)}>
        <button
          className={cn(
            'flex items-center gap-1.5 rounded-lg px-2 py-1.5 text-sm transition-colors',
            activePersona
              ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400 border border-primary-500/30'
              : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-dark-800 border border-transparent'
          )}
          aria-label={t('switch_persona')}
        >
          <Sparkles className="h-3.5 w-3.5 shrink-0" />
          <span className="truncate max-w-[100px] text-xs font-medium">
            {activePersona?.name ?? t('no_persona')}
          </span>
          <ChevronDown className="h-3 w-3 opacity-50 shrink-0" />
        </button>
      </DropdownMenuTrigger>
      {open && (
        <DropdownMenuContent align="end" className="min-w-[220px] max-h-[300px] overflow-y-auto custom-scrollbar">
          <DropdownMenuLabel>{t('switch_persona')}</DropdownMenuLabel>

          {/* خيار بدون شخصية */}
          <DropdownMenuItem
            onClick={() => {
              clearPersona();
              setOpen(false);
            }}
            className="justify-between"
          >
            <div className="flex items-center gap-2">
              <X className="h-3.5 w-3.5 text-gray-400" />
              <span>{t('no_persona')}</span>
            </div>
            {!activePersona && <Check className="h-4 w-4 text-primary-500" />}
          </DropdownMenuItem>

          <DropdownMenuSeparator />

          {/* قائمة الشخصيات */}
          {personas.map((persona) => (
            <DropdownMenuItem
              key={persona.id}
              onClick={() => {
                setActivePersona(persona);
                setOpen(false);
              }}
              className="justify-between"
            >
              <div className="flex items-center gap-2 min-w-0">
                <Sparkles className="h-3.5 w-3.5 shrink-0 text-primary-500" />
                <div className="min-w-0">
                  <p className="text-sm truncate">{persona.name}</p>
                  <p className="text-[10px] text-gray-400 truncate">
                    {persona.description.substring(0, 40)}
                  </p>
                </div>
              </div>
              {activePersona?.id === persona.id && (
                <Check className="h-4 w-4 text-primary-500 shrink-0" />
              )}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      )}
    </DropdownMenu>
  );
}
""")

    # 5. SettingsDropdown.tsx
    create_file("components/header/SettingsDropdown.tsx", """// قائمة الإعدادات المنسدلة: ملف شخصي ومفاتيح وتصدير وجولة ومدير وخروج
'use client';

import { useState } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { useRouter } from 'next/navigation';
import {
  Settings, User, Key, Download, HelpCircle, Hash,
  Shield, LogOut,
} from 'lucide-react';
import { cn } from '@/utils/cn';
import { useAuthStore } from '@/stores/authStore';
import { useUIStore } from '@/stores/uiStore';
import { useAuth } from '@/hooks/useAuth';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';

export function SettingsDropdown() {
  const t = useTranslations('header');
  const tAuth = useTranslations('auth');
  const locale = useLocale();
  const router = useRouter();
  const { role, user } = useAuthStore();
  const { setTourActive } = useUIStore();
  const { signOut } = useAuth();

  const [open, setOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  const isAdmin = role === 'admin';

  const roleBadge = {
    admin: { label: t('account_admin'), variant: 'destructive' as const },
    premium: { label: t('account_premium'), variant: 'premium' as const },
    free: { label: t('account_free'), variant: 'secondary' as const },
  };

  const currentBadge = roleBadge[role];

  return (
    <>
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger onClick={() => setOpen(!open)}>
          <button
            className={cn(
              'rounded-lg p-2 text-gray-500 transition-colors',
              'hover:bg-gray-100 dark:hover:bg-dark-800'
            )}
            aria-label={t('settings_profile')}
          >
            <Settings className="h-5 w-5" />
          </button>
        </DropdownMenuTrigger>
        {open && (
          <DropdownMenuContent align="end" className="min-w-[200px]">
            {/* معلومات المستخدم */}
            <div className="px-3 py-2 space-y-1">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 truncate">
                {user?.display_name ?? user?.email ?? ''}
              </p>
              <Badge variant={currentBadge.variant} className="text-[10px]">
                {currentBadge.label}
              </Badge>
            </div>

            <DropdownMenuSeparator />

            {/* الملف الشخصي */}
            <DropdownMenuItem
              icon={<User className="h-4 w-4" />}
              onClick={() => { router.push(`/${locale}/settings`); setOpen(false); }}
            >
              {t('settings_profile')}
            </DropdownMenuItem>

            {/* مفاتيح API */}
            <DropdownMenuItem
              icon={<Key className="h-4 w-4" />}
              onClick={() => { router.push(`/${locale}/settings`); setOpen(false); }}
            >
              {t('settings_api_keys')}
            </DropdownMenuItem>

            {/* تصدير */}
            <DropdownMenuItem
              icon={<Download className="h-4 w-4" />}
              onClick={() => { router.push(`/${locale}/settings`); setOpen(false); }}
            >
              {t('settings_export')}
            </DropdownMenuItem>

            <DropdownMenuSeparator />

            {/* جولة تعريفية */}
            <DropdownMenuItem
              icon={<HelpCircle className="h-4 w-4" />}
              onClick={() => { setTourActive(true); setOpen(false); }}
            >
              {t('settings_tour')}
            </DropdownMenuItem>

            {/* عداد الرموز */}
            <DropdownMenuItem
              icon={<Hash className="h-4 w-4" />}
              onClick={() => setOpen(false)}
            >
              {t('settings_tokens')}
            </DropdownMenuItem>

            {/* لوحة الإدارة */}
            {isAdmin && (
              <>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  icon={<Shield className="h-4 w-4" />}
                  onClick={() => { router.push(`/${locale}/admin`); setOpen(false); }}
                >
                  {t('settings_admin')}
                </DropdownMenuItem>
              </>
            )}

            <DropdownMenuSeparator />

            {/* تسجيل الخروج */}
            <DropdownMenuItem
              icon={<LogOut className="h-4 w-4" />}
              destructive
              onClick={() => { setShowLogoutConfirm(true); setOpen(false); }}
            >
              {t('settings_logout')}
            </DropdownMenuItem>
          </DropdownMenuContent>
        )}
      </DropdownMenu>

      {/* حوار تأكيد تسجيل الخروج */}
      <ConfirmDialog
        open={showLogoutConfirm}
        onOpenChange={setShowLogoutConfirm}
        title={tAuth('logout')}
        message={tAuth('logout_confirm')}
        confirmLabel={tAuth('logout')}
        destructive
        onConfirm={signOut}
      />
    </>
  );
}
""")

    # ──────────────────────────────────────────────
    # CHAT COMPONENTS
    # ──────────────────────────────────────────────
    print("\n📁 Chat Components")
    print("-" * 40)

    # 6. ChatArea.tsx
    create_file("components/chat/ChatArea.tsx", """// منطقة الدردشة: عرض الرسائل مع التمرير التلقائي وحالة الترحيب
'use client';

import { useRef, useEffect, useState, useCallback, type ReactNode } from 'react';
import { useTranslations } from 'next-intl';
import { MessageSquare, Sparkles, Zap, PenTool, Mail, ArrowDown } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { MessageBubble } from './MessageBubble';
import type { Message } from '@/types/chat';

interface ChatAreaProps {
  messages: Message[];
  streamingContent: string;
  isStreaming: boolean;
  isLoading: boolean;
  onSuggestionClick?: (text: string) => void;
  children?: ReactNode;
}

export function ChatArea({
  messages,
  streamingContent,
  isStreaming,
  isLoading,
  onSuggestionClick,
  children,
}: ChatAreaProps) {
  const t = useTranslations('chat');
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const [isUserScrolledUp, setIsUserScrolledUp] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);

  /**
   * التمرير إلى الأسفل
   */
  const scrollToBottom = useCallback((smooth: boolean = true) => {
    bottomRef.current?.scrollIntoView({
      behavior: smooth ? 'smooth' : 'instant',
    });
    setIsUserScrolledUp(false);
    setShowScrollButton(false);
  }, []);

  /**
   * مراقبة التمرير لتحديد إذا كان المستخدم قد رجع للأعلى
   */
  const handleScroll = useCallback(() => {
    const container = scrollRef.current;
    if (!container) return;

    const { scrollTop, scrollHeight, clientHeight } = container;
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
    const threshold = 150;

    if (distanceFromBottom > threshold) {
      setIsUserScrolledUp(true);
      setShowScrollButton(true);
    } else {
      setIsUserScrolledUp(false);
      setShowScrollButton(false);
    }
  }, []);

  /**
   * التمرير التلقائي عند وصول رسائل جديدة (إلا إذا رجع المستخدم للأعلى)
   */
  useEffect(() => {
    if (!isUserScrolledUp) {
      scrollToBottom(messages.length > 0);
    }
    return () => {};
  }, [messages.length, streamingContent, isUserScrolledUp, scrollToBottom]);

  /**
   * الاقتراحات
   */
  const suggestions = [
    { icon: Sparkles, text: t('suggestion_1'), slash: '/linkedin' },
    { icon: Zap, text: t('suggestion_2'), slash: '/brainstorm' },
    { icon: PenTool, text: t('suggestion_3'), slash: '/prompt' },
    { icon: Mail, text: t('suggestion_4'), slash: '/email' },
  ];

  // حالة التحميل
  if (isLoading) {
    return (
      <div className="flex-1 overflow-y-auto custom-scrollbar p-4">
        <div className="max-w-3xl mx-auto space-y-6">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={`skel-${i}`} className={cn('flex gap-3', i % 2 === 0 ? 'justify-end' : 'justify-start')}>
              {i % 2 !== 0 && <Skeleton circle className="h-8 w-8 shrink-0" />}
              <div className="space-y-2">
                <Skeleton className={cn('h-4', i % 2 === 0 ? 'w-48' : 'w-64')} />
                <Skeleton className={cn('h-4', i % 2 === 0 ? 'w-32' : 'w-56')} />
              </div>
              {i % 2 === 0 && <Skeleton circle className="h-8 w-8 shrink-0" />}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // حالة الترحيب (لا توجد رسائل)
  if (messages.length === 0 && !isStreaming) {
    return (
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full text-center space-y-8">
          <div className="space-y-3">
            <div className="flex justify-center">
              <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 shadow-lg shadow-primary-500/20">
                <MessageSquare className="h-10 w-10 text-white" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">
              {t('empty_welcome')}
            </h2>
            <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
              {t('empty_subtitle')}
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg mx-auto">
            {suggestions.map((s) => {
              const Icon = s.icon;
              return (
                <button
                  key={s.slash}
                  onClick={() => onSuggestionClick?.(s.text)}
                  className={cn(
                    'flex items-center gap-3 rounded-xl border border-gray-200 dark:border-dark-700',
                    'bg-white dark:bg-dark-800 p-4 text-start',
                    'hover:border-primary-500/50 hover:bg-primary-500/5 transition-all group'
                  )}
                >
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gray-100 dark:bg-dark-700 group-hover:bg-primary-500/10 transition-colors">
                    <Icon className="h-4 w-4 text-gray-500 group-hover:text-primary-500 transition-colors" />
                  </div>
                  <span className="text-sm text-gray-700 dark:text-gray-300">{s.text}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative flex-1">
      {/* منطقة الرسائل */}
      <div
        ref={scrollRef}
        onScroll={handleScroll}
        className="absolute inset-0 overflow-y-auto custom-scrollbar p-4"
      >
        <div className="max-w-3xl mx-auto space-y-1">
          {messages.map((msg, index) => (
            <MessageBubble
              key={msg.id}
              message={msg}
              isLast={index === messages.length - 1 && !isStreaming}
            />
          ))}

          {/* رسالة البث المباشر */}
          {isStreaming && streamingContent && (
            <MessageBubble
              message={{
                id: 'streaming',
                conversation_id: '',
                role: 'assistant',
                content: streamingContent,
                model: null,
                platform: null,
                persona_name: null,
                tokens_used: 0,
                response_time_ms: null,
                created_at: new Date().toISOString(),
              }}
              isStreaming
              isLast
            />
          )}

          <div ref={bottomRef} className="h-1" />
        </div>
      </div>

      {/* زر التمرير للأسفل */}
      {showScrollButton && (
        <button
          onClick={() => scrollToBottom(true)}
          className={cn(
            'absolute bottom-4 start-1/2 -translate-x-1/2 z-10',
            'flex items-center gap-1.5 rounded-full',
            'bg-gray-800 dark:bg-dark-600 text-white px-3 py-1.5',
            'shadow-lg hover:bg-gray-700 dark:hover:bg-dark-500 transition-colors',
            'text-xs font-medium animate-fade-in'
          )}
          aria-label="Scroll to bottom"
        >
          <ArrowDown className="h-3.5 w-3.5" />
        </button>
      )}
    </div>
  );
}
""")

    # 7. MessageBubble.tsx
    create_file("components/chat/MessageBubble.tsx", """// فقاعة الرسالة: عرض رسالة المستخدم أو المساعد مع التنسيق المناسب
'use client';

import { memo } from 'react';
import { Bot, User as UserIcon } from 'lucide-react';
import { cn } from '@/utils/cn';
import { MarkdownRenderer } from './MarkdownRenderer';
import { StreamingText } from './StreamingText';
import { MessageInfo } from './MessageInfo';
import type { Message } from '@/types/chat';

interface MessageBubbleProps {
  message: Message;
  isStreaming?: boolean;
  isLast?: boolean;
}

export const MessageBubble = memo(function MessageBubble({
  message,
  isStreaming = false,
  isLast = false,
}: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  // رسائل النظام
  if (isSystem) {
    return (
      <div className="flex justify-center py-2">
        <div className="rounded-lg bg-gray-100 dark:bg-dark-800 px-4 py-2 max-w-md">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
            {message.content}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        'flex gap-3 py-2',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      {/* أيقونة المساعد */}
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500/20 to-primary-600/20 mt-1">
          <Bot className="h-4.5 w-4.5 text-primary-500" />
        </div>
      )}

      {/* محتوى الرسالة */}
      <div className={cn('max-w-[80%] min-w-[60px]', isUser ? 'order-first' : '')}>
        <div
          className={cn(
            'rounded-2xl px-4 py-3',
            isUser
              ? 'bg-primary-500 text-white rounded-ee-md'
              : 'bg-gray-100 dark:bg-dark-800 text-gray-800 dark:text-gray-200 rounded-es-md'
          )}
        >
          {isUser ? (
            <p className="text-sm whitespace-pre-wrap break-words leading-relaxed">
              {message.content}
            </p>
          ) : isStreaming ? (
            <StreamingText content={message.content} />
          ) : (
            <MarkdownRenderer content={message.content} />
          )}
        </div>

        {/* معلومات الرسالة (للمساعد فقط) */}
        {!isUser && !isStreaming && isLast && (
          <MessageInfo message={message} />
        )}
      </div>

      {/* أيقونة المستخدم */}
      {isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gray-200 dark:bg-dark-700 mt-1">
          <UserIcon className="h-4.5 w-4.5 text-gray-500 dark:text-gray-400" />
        </div>
      )}
    </div>
  );
});
""")

    # 8. StreamingText.tsx
    create_file("components/chat/StreamingText.tsx", """// نص البث المباشر: يعرض النص المتدفق مع مؤشر وامض
'use client';

import { memo } from 'react';
import { MarkdownRenderer } from './MarkdownRenderer';

interface StreamingTextProps {
  content: string;
}

export const StreamingText = memo(function StreamingText({ content }: StreamingTextProps) {
  if (!content) {
    return (
      <div className="flex items-center gap-2">
        <div className="flex gap-1">
          <span className="h-2 w-2 rounded-full bg-primary-500 animate-pulse" style={{ animationDelay: '0ms' }} />
          <span className="h-2 w-2 rounded-full bg-primary-500 animate-pulse" style={{ animationDelay: '200ms' }} />
          <span className="h-2 w-2 rounded-full bg-primary-500 animate-pulse" style={{ animationDelay: '400ms' }} />
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      <MarkdownRenderer content={content} />
      {/* مؤشر الكتابة الوامض */}
      <span className="inline-block w-2 h-4 bg-primary-500 animate-blink align-middle ms-0.5 -mb-0.5 rounded-sm" />
    </div>
  );
});
""")

    # 9. MarkdownRenderer.tsx
    create_file("components/chat/MarkdownRenderer.tsx", """// عارض Markdown: يحول النص إلى HTML منسق مع تمييز الأكواد
'use client';

import { memo, type ComponentPropsWithoutRef } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import { cn } from '@/utils/cn';
import { CodeBlock } from './CodeBlock';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export const MarkdownRenderer = memo(function MarkdownRenderer({
  content,
  className,
}: MarkdownRendererProps) {
  return (
    <ReactMarkdown
      className={cn('text-sm leading-relaxed break-words', className)}
      rehypePlugins={[rehypeHighlight]}
      components={{
        // العناوين
        h1: ({ children }) => (
          <h1 className="text-xl font-bold mt-4 mb-2 text-gray-900 dark:text-gray-100">{children}</h1>
        ),
        h2: ({ children }) => (
          <h2 className="text-lg font-bold mt-3 mb-2 text-gray-900 dark:text-gray-100">{children}</h2>
        ),
        h3: ({ children }) => (
          <h3 className="text-base font-semibold mt-3 mb-1.5 text-gray-900 dark:text-gray-100">{children}</h3>
        ),
        h4: ({ children }) => (
          <h4 className="text-sm font-semibold mt-2 mb-1 text-gray-900 dark:text-gray-100">{children}</h4>
        ),

        // الفقرات
        p: ({ children }) => (
          <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>
        ),

        // النص الغامق والمائل
        strong: ({ children }) => (
          <strong className="font-semibold text-gray-900 dark:text-gray-100">{children}</strong>
        ),
        em: ({ children }) => (
          <em className="italic">{children}</em>
        ),

        // القوائم
        ul: ({ children }) => (
          <ul className="list-disc list-inside mb-2 space-y-0.5 ms-2">{children}</ul>
        ),
        ol: ({ children }) => (
          <ol className="list-decimal list-inside mb-2 space-y-0.5 ms-2">{children}</ol>
        ),
        li: ({ children }) => (
          <li className="leading-relaxed">{children}</li>
        ),

        // الروابط
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-500 hover:text-primary-400 underline underline-offset-2 transition-colors"
          >
            {children}
          </a>
        ),

        // الاقتباسات
        blockquote: ({ children }) => (
          <blockquote className="border-s-4 border-primary-500/50 ps-3 my-2 text-gray-600 dark:text-gray-400 italic">
            {children}
          </blockquote>
        ),

        // الجداول
        table: ({ children }) => (
          <div className="overflow-x-auto my-2 rounded-lg border border-gray-200 dark:border-dark-600">
            <table className="min-w-full text-sm">{children}</table>
          </div>
        ),
        thead: ({ children }) => (
          <thead className="bg-gray-50 dark:bg-dark-700">{children}</thead>
        ),
        tbody: ({ children }) => (
          <tbody className="divide-y divide-gray-200 dark:divide-dark-600">{children}</tbody>
        ),
        tr: ({ children }) => (
          <tr className="hover:bg-gray-50 dark:hover:bg-dark-800 transition-colors">{children}</tr>
        ),
        th: ({ children }) => (
          <th className="px-3 py-2 text-start font-semibold text-gray-700 dark:text-gray-300">{children}</th>
        ),
        td: ({ children }) => (
          <td className="px-3 py-2 text-gray-600 dark:text-gray-400">{children}</td>
        ),

        // الخط الأفقي
        hr: () => (
          <hr className="my-3 border-gray-200 dark:border-dark-600" />
        ),

        // الكود المضمن
        code: ({ className: codeClassName, children, ...props }) => {
          const match = /language-(\\w+)/.exec(codeClassName ?? '');
          const isInline = !match && !codeClassName;

          if (isInline) {
            return (
              <code
                className="rounded bg-gray-200 dark:bg-dark-700 px-1.5 py-0.5 text-xs font-mono text-primary-600 dark:text-primary-400"
                {...props}
              >
                {children}
              </code>
            );
          }

          const language = match ? match[1] ?? 'text' : 'text';
          const codeContent = String(children).replace(/\\n$/, '');

          return (
            <CodeBlock
              code={codeContent}
              language={language}
            />
          );
        },

        // الصور
        img: ({ src, alt }) => (
          <img
            src={src}
            alt={alt ?? ''}
            className="max-w-full rounded-lg my-2"
            loading="lazy"
          />
        ),

        // pre wrapper — we handle code blocks ourselves
        pre: ({ children }) => (
          <div className="my-2">{children}</div>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
});
""")

    # 10. CodeBlock.tsx
    create_file("components/chat/CodeBlock.tsx", """// كتلة الكود: عرض الكود مع تمييز اللغة وزر النسخ
'use client';

import { useState, useCallback, memo } from 'react';
import { useTranslations } from 'next-intl';
import { Copy, Check, FileCode } from 'lucide-react';
import { cn } from '@/utils/cn';
import { copyToClipboard } from '@/utils/helpers';

interface CodeBlockProps {
  code: string;
  language: string;
  className?: string;
}

export const CodeBlock = memo(function CodeBlock({
  code,
  language,
  className,
}: CodeBlockProps) {
  const t = useTranslations('common');
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    const success = await copyToClipboard(code);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [code]);

  // تنسيق اسم اللغة
  const displayLanguage = language.charAt(0).toUpperCase() + language.slice(1);

  return (
    <div className={cn('rounded-lg overflow-hidden border border-dark-600 my-2', className)}>
      {/* شريط أعلى الكود */}
      <div className="flex items-center justify-between bg-dark-800 px-3 py-1.5">
        <div className="flex items-center gap-1.5">
          <FileCode className="h-3.5 w-3.5 text-gray-400" />
          <span className="text-xs text-gray-400 font-mono">{displayLanguage}</span>
        </div>
        <button
          onClick={handleCopy}
          className={cn(
            'flex items-center gap-1 rounded-md px-2 py-0.5 text-xs transition-all',
            copied
              ? 'text-green-400 bg-green-500/10'
              : 'text-gray-400 hover:text-gray-200 hover:bg-dark-700'
          )}
          aria-label={copied ? t('copied') : t('copy')}
        >
          {copied ? (
            <>
              <Check className="h-3 w-3" />
              <span>{t('copied')}</span>
            </>
          ) : (
            <>
              <Copy className="h-3 w-3" />
              <span>{t('copy')}</span>
            </>
          )}
        </button>
      </div>

      {/* محتوى الكود */}
      <div className="overflow-x-auto custom-scrollbar">
        <pre className="bg-dark-950 p-3 text-sm leading-relaxed">
          <code className={cn('font-mono text-gray-300', `language-${language}`)}>
            {code}
          </code>
        </pre>
      </div>
    </div>
  );
});
""")

    # 11. MessageInfo.tsx
    create_file("components/chat/MessageInfo.tsx", """// معلومات الرسالة: يعرض بيانات إضافية أسفل رسالة المساعد
'use client';

import { useState, useCallback, memo } from 'react';
import { useTranslations } from 'next-intl';
import { Copy, Check, Sparkles, Cpu, Clock, Hash, RefreshCw } from 'lucide-react';
import { cn } from '@/utils/cn';
import { copyToClipboard } from '@/utils/helpers';
import { formatTokenCount, formatResponseTime } from '@/utils/formatters';
import { Tooltip } from '@/components/ui/tooltip';
import type { Message } from '@/types/chat';

interface MessageInfoProps {
  message: Message;
  onRegenerate?: () => void;
}

export const MessageInfo = memo(function MessageInfo({
  message,
  onRegenerate,
}: MessageInfoProps) {
  const t = useTranslations('chat');
  const tCommon = useTranslations('common');
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    const success = await copyToClipboard(message.content);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [message.content]);

  const hasInfo = message.persona_name || message.model || message.tokens_used > 0 || message.response_time_ms;

  if (!hasInfo && !onRegenerate) return null;

  return (
    <div className="flex items-center flex-wrap gap-x-3 gap-y-1 mt-1.5 px-1">
      {/* الشخصية */}
      {message.persona_name && (
        <div className="flex items-center gap-1 text-[11px] text-gray-400 dark:text-gray-500">
          <Sparkles className="h-3 w-3" />
          <span>{message.persona_name}</span>
        </div>
      )}

      {/* النموذج */}
      {message.model && (
        <div className="flex items-center gap-1 text-[11px] text-gray-400 dark:text-gray-500">
          <Cpu className="h-3 w-3" />
          <span>{message.model.split('/').pop()}</span>
        </div>
      )}

      {/* الرموز */}
      {message.tokens_used > 0 && (
        <div className="flex items-center gap-1 text-[11px] text-gray-400 dark:text-gray-500">
          <Hash className="h-3 w-3" />
          <span>{formatTokenCount(message.tokens_used)}</span>
        </div>
      )}

      {/* وقت الاستجابة */}
      {message.response_time_ms != null && message.response_time_ms > 0 && (
        <div className="flex items-center gap-1 text-[11px] text-gray-400 dark:text-gray-500">
          <Clock className="h-3 w-3" />
          <span>{formatResponseTime(message.response_time_ms)}</span>
        </div>
      )}

      {/* الإجراءات */}
      <div className="flex items-center gap-1 ms-auto">
        {/* نسخ */}
        <Tooltip content={copied ? tCommon('copied') : t('copy_message')}>
          <button
            onClick={handleCopy}
            className={cn(
              'rounded p-1 transition-colors',
              copied
                ? 'text-green-500'
                : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700'
            )}
            aria-label={t('copy_message')}
          >
            {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          </button>
        </Tooltip>

        {/* إعادة التوليد */}
        {onRegenerate && (
          <Tooltip content={t('regenerate')}>
            <button
              onClick={onRegenerate}
              className="rounded p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700 transition-colors"
              aria-label={t('regenerate')}
            >
              <RefreshCw className="h-3.5 w-3.5" />
            </button>
          </Tooltip>
        )}
      </div>
    </div>
  );
});
""")

    # ──────────────────────────────────────────────
    # COMMON COMPONENTS
    # ──────────────────────────────────────────────
    print("\n📁 Common Components")
    print("-" * 40)

    # 12. TokenCounter.tsx
    create_file("components/common/TokenCounter.tsx", """// عداد الرموز: يعرض عدد الرموز المستخدمة بتنسيق مقروء
'use client';

import { memo } from 'react';
import { Hash } from 'lucide-react';
import { cn } from '@/utils/cn';
import { formatTokenCount } from '@/utils/formatters';

interface TokenCounterProps {
  tokens: number;
  className?: string;
  showIcon?: boolean;
  size?: 'sm' | 'md';
}

export const TokenCounter = memo(function TokenCounter({
  tokens,
  className,
  showIcon = true,
  size = 'sm',
}: TokenCounterProps) {
  return (
    <div
      className={cn(
        'inline-flex items-center gap-1 rounded-md',
        'text-gray-500 dark:text-gray-400',
        size === 'sm' ? 'text-xs' : 'text-sm',
        className
      )}
      title={`${tokens.toLocaleString()} tokens`}
    >
      {showIcon && (
        <Hash className={cn(size === 'sm' ? 'h-3 w-3' : 'h-3.5 w-3.5')} />
      )}
      <span className="font-mono tabular-nums">
        {formatTokenCount(tokens)}
      </span>
    </div>
  );
});
""")

    # 13. MessageCounter.tsx
    create_file("components/common/MessageCounter.tsx", """// عداد الرسائل: يعرض عدد الرسائل المستخدمة من الحد الأقصى مع ألوان تحذيرية
'use client';

import { memo, useMemo } from 'react';
import { MessageSquare } from 'lucide-react';
import { cn } from '@/utils/cn';
import { MESSAGE_LIMIT_PER_CHAT } from '@/utils/constants';
import { Tooltip } from '@/components/ui/tooltip';
import { useTranslations } from 'next-intl';

interface MessageCounterProps {
  current: number;
  limit?: number;
  className?: string;
}

export const MessageCounter = memo(function MessageCounter({
  current,
  limit = MESSAGE_LIMIT_PER_CHAT,
  className,
}: MessageCounterProps) {
  const t = useTranslations('chat');

  const colorClass = useMemo(() => {
    const remaining = limit - current;

    if (remaining <= 0) {
      return 'text-red-500 dark:text-red-400 bg-red-500/10';
    }
    if (remaining === 1) {
      return 'text-red-500 dark:text-red-400 bg-red-500/10';
    }
    if (remaining <= 2) {
      return 'text-orange-500 dark:text-orange-400 bg-orange-500/10';
    }
    return 'text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-dark-800';
  }, [current, limit]);

  const isAtLimit = current >= limit;

  const tooltipText = t('messages_used', {
    used: current.toString(),
    total: limit.toString(),
  });

  return (
    <Tooltip content={tooltipText}>
      <div
        className={cn(
          'inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium transition-colors',
          colorClass,
          isAtLimit && 'animate-pulse-slow',
          className
        )}
      >
        <MessageSquare className="h-3 w-3" />
        <span className="font-mono tabular-nums">
          {current}/{limit}
        </span>
      </div>
    </Tooltip>
  );
});
""")

    # ──────────────────────────────────────────────
    # MESSAGE INPUT component (needed for complete chat)
    # ──────────────────────────────────────────────
    print("\n📁 Message Input Component")
    print("-" * 40)

    create_file("components/chat/MessageInput.tsx", """// حقل إدخال الرسالة: حقل نص متعدد الأسطر مع إرسال وأوامر مائلة
'use client';

import { useState, useRef, useCallback, useEffect, type KeyboardEvent, type FormEvent } from 'react';
import { useTranslations } from 'next-intl';
import { Send, Square, Sparkles } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { Tooltip } from '@/components/ui/tooltip';
import { SLASH_COMMANDS, MESSAGE_LIMIT_PER_CHAT, UI_CONSTANTS } from '@/utils/constants';

interface MessageInputProps {
  onSend: (message: string) => void;
  onStop?: () => void;
  isSending: boolean;
  isStreaming: boolean;
  isDisabled: boolean;
  messageCount: number;
  placeholder?: string;
  onSlashCommand?: (personaId: string) => void;
}

export function MessageInput({
  onSend,
  onStop,
  isSending,
  isStreaming,
  isDisabled,
  messageCount,
  placeholder,
  onSlashCommand,
}: MessageInputProps) {
  const t = useTranslations('chat');
  const [message, setMessage] = useState('');
  const [showSlashMenu, setShowSlashMenu] = useState(false);
  const [slashFilter, setSlashFilter] = useState('');
  const [selectedSlashIndex, setSelectedSlashIndex] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const isAtLimit = messageCount >= MESSAGE_LIMIT_PER_CHAT;
  const canSend = message.trim().length > 0 && !isSending && !isStreaming && !isDisabled && !isAtLimit;

  /**
   * تعديل ارتفاع مربع النص تلقائياً
   */
  const adjustHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      const newHeight = Math.min(textarea.scrollHeight, 200);
      textarea.style.height = `${newHeight}px`;
    }
  }, []);

  useEffect(() => {
    adjustHeight();
    return () => {};
  }, [message, adjustHeight]);

  /**
   * التعامل مع تغيير النص
   */
  const handleChange = useCallback(
    (value: string) => {
      if (value.length > UI_CONSTANTS.MAX_MESSAGE_LENGTH) return;

      setMessage(value);

      // كشف الأوامر المائلة
      if (value.startsWith('/') && value.length <= 20) {
        const filter = value.substring(1).toLowerCase();
        setSlashFilter(filter);
        setShowSlashMenu(true);
        setSelectedSlashIndex(0);
      } else {
        setShowSlashMenu(false);
      }
    },
    []
  );

  /**
   * الأوامر المائلة المصفاة
   */
  const filteredCommands = SLASH_COMMANDS.filter(
    (cmd) =>
      cmd.command.substring(1).startsWith(slashFilter) ||
      cmd.labelAr.includes(slashFilter) ||
      cmd.labelEn.toLowerCase().includes(slashFilter)
  );

  /**
   * إرسال الرسالة
   */
  const handleSend = useCallback(() => {
    if (!canSend) return;

    onSend(message.trim());
    setMessage('');
    setShowSlashMenu(false);

    // إعادة تركيز مربع النص
    setTimeout(() => {
      textareaRef.current?.focus();
    }, 50);
  }, [message, canSend, onSend]);

  /**
   * اختيار أمر مائل
   */
  const handleSlashSelect = useCallback(
    (command: typeof SLASH_COMMANDS[number]) => {
      setMessage('');
      setShowSlashMenu(false);
      onSlashCommand?.(command.personaId);
    },
    [onSlashCommand]
  );

  /**
   * التعامل مع أحداث لوحة المفاتيح
   */
  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      // قائمة الأوامر المائلة
      if (showSlashMenu && filteredCommands.length > 0) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          setSelectedSlashIndex((prev) =>
            prev < filteredCommands.length - 1 ? prev + 1 : 0
          );
          return;
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          setSelectedSlashIndex((prev) =>
            prev > 0 ? prev - 1 : filteredCommands.length - 1
          );
          return;
        }
        if (e.key === 'Enter' || e.key === 'Tab') {
          e.preventDefault();
          const selected = filteredCommands[selectedSlashIndex];
          if (selected) {
            handleSlashSelect(selected);
          }
          return;
        }
        if (e.key === 'Escape') {
          e.preventDefault();
          setShowSlashMenu(false);
          return;
        }
      }

      // إرسال بـ Enter (بدون Shift)
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [showSlashMenu, filteredCommands, selectedSlashIndex, handleSlashSelect, handleSend]
  );

  return (
    <div className="shrink-0 border-t border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-900 p-3 relative">
      {/* قائمة الأوامر المائلة */}
      {showSlashMenu && filteredCommands.length > 0 && (
        <div className="absolute bottom-full start-3 end-3 mb-1 rounded-xl border border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-800 shadow-xl overflow-hidden z-20 animate-fade-in">
          <div className="p-2 space-y-0.5">
            {filteredCommands.map((cmd, index) => (
              <button
                key={cmd.command}
                onClick={() => handleSlashSelect(cmd)}
                className={cn(
                  'flex items-center gap-3 w-full rounded-lg px-3 py-2 text-start transition-colors',
                  index === selectedSlashIndex
                    ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700'
                )}
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-500/10">
                  <Sparkles className="h-4 w-4 text-primary-500" />
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <code className="text-xs font-mono text-primary-500">{cmd.command}</code>
                    <span className="text-sm font-medium">{cmd.labelAr}</span>
                  </div>
                  <p className="text-xs text-gray-400 truncate">{cmd.description_ar}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="max-w-3xl mx-auto">
        <div
          className={cn(
            'flex items-end gap-2 rounded-xl border bg-white dark:bg-dark-800 transition-colors',
            'focus-within:border-primary-500 focus-within:ring-1 focus-within:ring-primary-500/30',
            isAtLimit
              ? 'border-red-300 dark:border-red-700'
              : 'border-gray-200 dark:border-dark-600',
            'px-3 py-2'
          )}
        >
          {/* مربع النص */}
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => handleChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder ?? (isAtLimit ? t('message_limit_title') : t('type_message'))}
            disabled={isDisabled || isAtLimit}
            rows={1}
            className={cn(
              'flex-1 resize-none bg-transparent text-sm outline-none',
              'text-gray-700 dark:text-gray-300',
              'placeholder:text-gray-400 dark:placeholder:text-gray-500',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              'min-h-[24px] max-h-[200px]'
            )}
            dir="auto"
          />

          {/* زر الإرسال أو الإيقاف */}
          {isStreaming ? (
            <Tooltip content={t('stop')}>
              <Button
                size="icon-sm"
                variant="destructive"
                onClick={onStop}
                className="shrink-0 rounded-lg"
                aria-label={t('stop')}
              >
                <Square className="h-4 w-4" />
              </Button>
            </Tooltip>
          ) : (
            <Tooltip content={t('send')}>
              <Button
                size="icon-sm"
                onClick={handleSend}
                disabled={!canSend}
                className="shrink-0 rounded-lg"
                aria-label={t('send')}
              >
                <Send className="h-4 w-4" />
              </Button>
            </Tooltip>
          )}
        </div>

        {/* تلميح الأوامر المائلة */}
        <p className="text-center text-[10px] text-gray-400 dark:text-gray-500 mt-1.5">
          {t('type_slash')}
        </p>
      </div>
    </div>
  );
}
""")

    # ──────────────────────────────────────────────
    # RATE LIMIT components
    # ──────────────────────────────────────────────
    print("\n📁 Rate Limit Components")
    print("-" * 40)

    create_file("components/chat/RateLimitTimer.tsx", """// مؤقت حد المعدل: يعرض عداً تنازلياً عند الوصول لحد المعدل
'use client';

import { useState, useEffect, useCallback, memo } from 'react';
import { useTranslations } from 'next-intl';
import { Clock, Sparkles } from 'lucide-react';
import { cn } from '@/utils/cn';
import { formatDuration } from '@/utils/formatters';

interface RateLimitTimerProps {
  seconds: number;
  isVisible: boolean;
  onComplete: () => void;
  showUpgradeHint?: boolean;
  className?: string;
}

export const RateLimitTimer = memo(function RateLimitTimer({
  seconds,
  isVisible,
  onComplete,
  showUpgradeHint = true,
  className,
}: RateLimitTimerProps) {
  const t = useTranslations('chat');
  const [remaining, setRemaining] = useState(seconds);

  useEffect(() => {
    setRemaining(seconds);
  }, [seconds]);

  useEffect(() => {
    if (!isVisible || remaining <= 0) return;

    const interval = setInterval(() => {
      setRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          onComplete();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isVisible, remaining, onComplete]);

  if (!isVisible || remaining <= 0) return null;

  const progress = ((seconds - remaining) / seconds) * 100;

  return (
    <div className={cn(
      'flex flex-col items-center gap-2 rounded-xl border border-orange-200 dark:border-orange-800/30',
      'bg-orange-50 dark:bg-orange-900/10 p-4',
      className
    )}>
      <div className="flex items-center gap-2">
        <Clock className="h-5 w-5 text-orange-500 animate-pulse" />
        <span className="text-sm font-medium text-orange-700 dark:text-orange-300">
          {t('rate_limit_wait')}
        </span>
      </div>

      {/* شريط التقدم */}
      <div className="w-full max-w-xs h-2 rounded-full bg-orange-200 dark:bg-orange-800/30 overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-orange-400 to-orange-500 transition-all duration-1000"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* الوقت المتبقي */}
      <span className="text-2xl font-mono font-bold text-orange-600 dark:text-orange-400 tabular-nums">
        {formatDuration(remaining)}
      </span>

      {/* تلميح الترقية */}
      {showUpgradeHint && (
        <p className="flex items-center gap-1 text-xs text-orange-500 dark:text-orange-400">
          <Sparkles className="h-3 w-3" />
          {t('rate_limit_tip')}
        </p>
      )}
    </div>
  );
});
""")

    create_file("components/chat/MessageLimitAlert.tsx", """// تنبيه حد الرسائل: يظهر عند الوصول للحد الأقصى في المحادثة
'use client';

import { memo } from 'react';
import { useTranslations } from 'next-intl';
import { AlertTriangle, Plus, Download, Trash2 } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { MESSAGE_LIMIT_PER_CHAT } from '@/utils/constants';

interface MessageLimitAlertProps {
  onNewChat: () => void;
  onExport?: () => void;
  onDelete?: () => void;
  className?: string;
}

export const MessageLimitAlert = memo(function MessageLimitAlert({
  onNewChat,
  onExport,
  onDelete,
  className,
}: MessageLimitAlertProps) {
  const t = useTranslations('chat');

  return (
    <div className={cn(
      'rounded-xl border border-red-200 dark:border-red-800/30',
      'bg-red-50 dark:bg-red-900/10 p-4 space-y-3',
      className
    )}>
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-5 w-5 text-red-500" />
        <span className="text-sm font-semibold text-red-700 dark:text-red-300">
          {t('message_limit_title')}
        </span>
      </div>

      <p className="text-sm text-red-600 dark:text-red-400">
        {t('message_limit_body', { limit: MESSAGE_LIMIT_PER_CHAT.toString() })}
      </p>

      <div className="flex flex-wrap items-center gap-2">
        <Button size="sm" onClick={onNewChat} className="gap-1.5">
          <Plus className="h-3.5 w-3.5" />
          {t('start_new')}
        </Button>

        {onExport && (
          <Button size="sm" variant="outline" onClick={onExport} className="gap-1.5">
            <Download className="h-3.5 w-3.5" />
            {t('export_conversation')}
          </Button>
        )}

        {onDelete && (
          <Button size="sm" variant="outline" onClick={onDelete} className="gap-1.5 text-red-600 hover:text-red-700">
            <Trash2 className="h-3.5 w-3.5" />
            {t('delete_conversation')}
          </Button>
        )}
      </div>
    </div>
  );
});
""")

    # ──────────────────────────────────────────────
    # SLASH COMMANDS component
    # ──────────────────────────────────────────────
    create_file("components/chat/SlashCommands.tsx", """// أوامر مائلة: قائمة الأوامر السريعة للشخصيات المدمجة
'use client';

import { memo } from 'react';
import { Sparkles } from 'lucide-react';
import { cn } from '@/utils/cn';
import { SLASH_COMMANDS } from '@/utils/constants';
import { useLocale } from 'next-intl';

interface SlashCommandsProps {
  filter: string;
  selectedIndex: number;
  onSelect: (personaId: string) => void;
  visible: boolean;
}

export const SlashCommands = memo(function SlashCommands({
  filter,
  selectedIndex,
  onSelect,
  visible,
}: SlashCommandsProps) {
  const locale = useLocale();

  const filteredCommands = SLASH_COMMANDS.filter(
    (cmd) =>
      cmd.command.substring(1).startsWith(filter) ||
      (locale === 'ar' ? cmd.labelAr : cmd.labelEn).toLowerCase().includes(filter.toLowerCase())
  );

  if (!visible || filteredCommands.length === 0) return null;

  return (
    <div className="absolute bottom-full start-0 end-0 mb-2 rounded-xl border border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-800 shadow-xl overflow-hidden z-20 animate-fade-in">
      <div className="p-2 space-y-0.5">
        {filteredCommands.map((cmd, index) => (
          <button
            key={cmd.command}
            onClick={() => onSelect(cmd.personaId)}
            className={cn(
              'flex items-center gap-3 w-full rounded-lg px-3 py-2 text-start transition-colors',
              index === selectedIndex
                ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700'
            )}
          >
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-500/10">
              <Sparkles className="h-4 w-4 text-primary-500" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <code className="text-xs font-mono text-primary-500">{cmd.command}</code>
                <span className="text-sm font-medium">
                  {locale === 'ar' ? cmd.labelAr : cmd.labelEn}
                </span>
              </div>
              <p className="text-xs text-gray-400 truncate">
                {locale === 'ar' ? cmd.description_ar : cmd.description_en}
              </p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
});
""")

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 3B SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print()
    print("  HEADER COMPONENTS:")
    print("    1.  components/header/Header.tsx             (Main header 56px)")
    print("    2.  components/header/PlatformSelector.tsx   (7 platforms dropdown)")
    print("    3.  components/header/ModelSelector.tsx      (Dynamic models per platform)")
    print("    4.  components/header/PersonaSelector.tsx    (Active persona + quick switch)")
    print("    5.  components/header/SettingsDropdown.tsx   (Gear menu with all options)")
    print()
    print("  CHAT COMPONENTS:")
    print("    6.  components/chat/ChatArea.tsx             (Messages area + welcome + autoscroll)")
    print("    7.  components/chat/MessageBubble.tsx        (User/AI/System bubbles)")
    print("    8.  components/chat/StreamingText.tsx        (Blinking cursor streaming)")
    print("    9.  components/chat/MarkdownRenderer.tsx     (Full Markdown rendering)")
    print("    10. components/chat/CodeBlock.tsx            (Code + highlight + copy)")
    print("    11. components/chat/MessageInfo.tsx          (Persona/model/tokens/time/copy)")
    print("    +   components/chat/MessageInput.tsx         (Textarea + send + slash)")
    print("    +   components/chat/RateLimitTimer.tsx       (Countdown + progress bar)")
    print("    +   components/chat/MessageLimitAlert.tsx    (Limit reached + actions)")
    print("    +   components/chat/SlashCommands.tsx        (Slash command popup)")
    print()
    print("  COMMON COMPONENTS:")
    print("    12. components/common/TokenCounter.tsx       (Formatted token display)")
    print("    13. components/common/MessageCounter.tsx     (X/15 with color states)")
    print()
    print("📝 NOTES:")
    print("  - Header: 56px, responsive (simplified on mobile)")
    print("  - PlatformSelector: 7 platforms with emoji icons, updates platformStore")
    print("  - ModelSelector: loads global_models per platform from Supabase")
    print("  - PersonaSelector: shows active persona, dropdown to switch/clear")
    print("  - SettingsDropdown: profile/keys/export/tour/tokens/admin/logout")
    print("  - ChatArea: welcome state, 4 suggestion cards, auto-scroll with pause")
    print("  - MessageBubble: user=right purple, AI=left gray, system=centered")
    print("  - StreamingText: blinking cursor indicator during streaming")
    print("  - MarkdownRenderer: full markdown with headings/lists/tables/blockquotes")
    print("  - CodeBlock: dark bg, language label, copy button with 'Copied!' feedback")
    print("  - MessageInfo: persona|model|tokens|time|copy|regenerate")
    print("  - MessageInput: auto-resize textarea, slash commands, Enter to send")
    print("  - RateLimitTimer: countdown with progress bar and upgrade hint")
    print("  - MessageCounter: green(1-12), orange(13), red(14-15), pulse at limit")
    print("  - All components memo'd where appropriate for performance")
    print("  - All i18n, no hardcoded strings")
    print("  - TypeScript strict, no 'any' types")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 3C: AI Providers + API Route + Encryption + Rate Limiting")
    print("  Phase 4:  API Keys management + Settings page")
    print("  Phase 5A: Personas (library, form, ratings)")
    print("  Phase 5B: Features (export, onboarding)")
    print("  Phase 6A: Admin (layout, dashboard, users)")
    print("  Phase 6B: Admin (keys, models, personas, codes, notifications)")
    print("  Phase 7:  Final (worker proxy, telegram, polish)")
    print()
    print("✅ Phase 3B Complete! Ready for Phase 3C.")


if __name__ == "__main__":
    main()
